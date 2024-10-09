import io
import json
import logging
import os
import re
import gzip
from datetime import datetime, timezone

from fdk import context, response
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from helpers import get_metric_name,get_metric_attributes, get_metric_points, _should_compress_payload


logger = logging.getLogger(__name__)


OUTPUT_MESSAGE_VERSION = "v1.0"

_max_pool = int(os.environ.get("CHRONO_MAX_POOL", 10))
_session = requests.Session()
_session.mount("https://", HTTPAdapter(pool_connections=_max_pool))

def handler(ctx: context.InvokeContext, data: io.BytesIO = None) -> response.Response:
    """
    OCI Function Entry Point
    :param ctx: InvokeContext
    :param data: OCI metric payload
    :return: HTTP 200 response
    """

    try:
        serialized_metric_data = _get_serialized_metric_data(data)
        metrics_message = _generate_metrics_msg(ctx, serialized_metric_data)
        result = _send_metrics_msg_to_otel_collector(metrics_message)
    except HTTPError as e:
        logger.exception(f"Error sending metrics to OTel Collector")
        result = e.response.text
    except Exception as e:
        logger.exception("Unexpected error while processing input data")
        result = str(e)

    return response.Response(
        ctx,
        response_data=json.dumps({"result": result}),
        headers={"Content-Type": "application/json"},
    )

def _get_serialized_metric_data(raw_metrics: io.BytesIO) -> str:
    return raw_metrics.getvalue().decode("utf-8")

def _generate_metrics_msg(
    ctx: context.InvokeContext,
    serialized_metric_data: str,
) -> str:
    logger.info(f"Serialized metric data: {serialized_metric_data}")

    # Use OCI Function application ID for required service.instance.id attribute
    source_fn_app_ocid = ctx.AppID()
    # Use "oci" for required service.name attribute
    service_name = "oci"
    metrics_list = json.loads(serialized_metric_data)
    converted_event_list = handle_metric_events(event_list=metrics_list)

    result = {
        "resourceMetrics": [
            {
            "resource": {
                "attributes": [
                {
                    "key": "service.name",
                    "value": {
                    "stringValue": service_name
                    }
                },
                {
                    "key": "service.instance.id",
                    "value": {
                    "stringValue": source_fn_app_ocid
                    }
                }
                ]
            },
            "scopeMetrics": [
                {
                    "metrics": converted_event_list
                }
            ]
            }
        ]
    }

    # OTLP format must be in lowercase
    return json.dumps(result).replace('True', 'true').replace('False', 'false')

def handle_metric_events(event_list):
    """
    :param event_list: list of OCI-formatted log records.
    :return: list of OTLP-formatted log records
    """

    result_list = []
    for event in event_list:
        single_result = transform_metric_to_otlp_format(log_record=event)
        result_list.append(single_result)

    return result_list

def transform_metric_to_otlp_format(log_record: dict):
    """
    Example OTLP payload: https://github.com/open-telemetry/opentelemetry-proto/blob/main/examples/metrics.json
    """

    metric_name = get_metric_name(log_record)
    metric_attributes = get_metric_attributes(log_record)
    metric_points = get_metric_points(log_record, metric_attributes)
    with open('./data/metric_types.json', 'r') as f:
        metric_types = json.load(f)
    
    result = {
        "name": metric_name
    }

    if metric_name in metric_types:
        metric_type = metric_types[metric_name]["metric_type"]
        
        if metric_type == "cumulative_counter":
            result["sum"] = {
                "isMonotonic": True,
                "aggregationTemporality": 2,
                "dataPoints": metric_points
            }
        elif metric_type == "delta_counter":
            result["sum"] = {
                "isMonotonic": True,
                "aggregationTemporality": 1,
                "dataPoints": metric_points
            }
        else:
            result[metric_type] = {
                "dataPoints": metric_points
            }
    
    return result

def _send_metrics_msg_to_otel_collector(metrics_message: str) -> str:
    otel_endpoint = os.environ.get("OTEL_ENDPOINT")
    api_headers = {"content-type": "application/json"}

    if _should_compress_payload():
        serialized = gzip.compress(metrics_message.encode())
        api_headers["content-encoding"] = "gzip"
    else:
        serialized = metrics_message

    http_response = _session.post(
        otel_endpoint, 
        data=serialized, 
        headers=api_headers
    )

    http_response.raise_for_status()
    logger.info(
        f"Sent payload size={len(metrics_message)} encoding={api_headers.get('content-encoding', None)}"
    )
    return http_response.text