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


logger = logging.getLogger(__name__)


OUTPUT_MESSAGE_VERSION = "v1.0"

_max_pool = int(os.environ.get("DD_MAX_POOL", 10))
_session = requests.Session()
_session.mount("https://", HTTPAdapter(pool_connections=_max_pool))


def _get_serialized_metric_data(raw_metrics: io.BytesIO) -> str:
    return raw_metrics.getvalue().decode("utf-8")

def _generate_metrics_msg(
    ctx: context.InvokeContext,
    serialized_metric_data: str,
) -> str:
    logger.info(f"Serialized metric data: {serialized_metric_data}")

    # Get service instance id (using value of tenancy ocid for now)
    tenancy_ocid = os.environ.get("TENANCY_OCID")
    # tenancy_ocid = "test-tenancy-ocid"
    if not tenancy_ocid:
        raise ValueError("Missing environment variable: TENANCY_OCID")

    # Get service name (using value of "oci" for now)
    service_name = "oci"
    # Get metrics
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
                    "stringValue": tenancy_ocid
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
    :param event_list: the list of OCI-formatted log records.
    :return: the list of OTLP-formatted log records
    """

    result_list = []
    for event in event_list:
        single_result = transform_metric_to_otlp_format(log_record=event)
        result_list.append(single_result)

    return result_list

def transform_metric_to_otlp_format(log_record: dict):
    """
    Transforms a metric from OCI to OTLP format. 
    Example OTLP payload: https://github.com/open-telemetry/opentelemetry-proto/blob/main/examples/metrics.json
    :param log_record: metric log record
    :return: OTLP-formatted log record
    """
    # Get metric name
    metric_name = get_metric_name(log_record)

    # Get metric values
    metric_points = get_metric_points(log_record)

    # Get metric type
    with open('metrics_mapping.json', 'r') as f:
        metrics_mapping = json.load(f)
    
    result = {
        "name": metric_name
    }

    if metric_name in metrics_mapping:
        metric_type = metrics_mapping[metric_name]

        if metric_type == "sum":
            result[metric_type] = {
                "aggregationTemporality": 1,
                "isMonotonic": True,
                "dataPoints": metric_points
            }
        else:
            result[metric_type] = {
                "dataPoints": metric_points
            }
    
    return result

def get_metric_name(log_record: dict):
    """
    Assembles a metric name
    :param log_record:
    :return:
    """

    elements = get_dictionary_value(log_record, 'namespace').split('_')
    elements += camel_case_split(get_dictionary_value(log_record, 'name'))
    elements = [element.lower() for element in elements]
    return '.'.join(elements)

def camel_case_split(str):
    """
    :param str:
    :return: Splits camel case string to individual strings
    """

    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)

def get_metric_points(log_record: dict):
    """
    :param log_record:
    :return: an array of arrays where each array is a datapoint scalar pair
    """

    result = []

    datapoints = get_dictionary_value(dictionary=log_record, target_key='datapoints')
    for point in datapoints:
        # Calculate required TimeUnixNano
        # Skipped recommended StartTimeUnixNano since only using Gauges (for now)
        unix_timestamp_nano_str = str(int(point.get('timestamp')) * 1_000_000)

        dd_point = {'asDouble': point.get('value'),
                    'timeUnixNano': unix_timestamp_nano_str}

        result.append(dd_point)

    return result

def get_dictionary_value(dictionary: dict, target_key: str):
    """
    Recursive method to find value within a dictionary which may also have nested lists / dictionaries.
    :param dictionary: the dictionary to scan
    :param target_key: the key we are looking for
    :return: If a target_key exists multiple times in the dictionary, the first one found will be returned.
    """

    if dictionary is None:
        raise Exception('dictionary None for key'.format(target_key))

    target_value = dictionary.get(target_key)
    if target_value:
        return target_value

    for key, value in dictionary.items():
        if isinstance(value, dict):
            target_value = get_dictionary_value(dictionary=value, target_key=target_key)
            if target_value:
                return target_value

        elif isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict):
                    target_value = get_dictionary_value(dictionary=entry, target_key=target_key)
                    if target_value:
                        return target_value
                        
def _should_compress_payload() -> bool:
    return os.environ.get("DD_COMPRESS", "false").lower() == "true"


def _send_metrics_msg_to_datadog(metrics_message: str) -> str:
    # url = f"https://enxtvhswcvxv.x.pipedream.net"
    url = f"https://wondrous-touched-fish.ngrok-free.app/v1/metrics"
    api_headers = {"content-type": "application/json"}

    # if _should_compress_payload():
    #     serialized = gzip.compress(metrics_message.encode())
    #     api_headers["content-encoding"] = "gzip"
    # else:
    #     serialized = metrics_message

    http_response = _session.post(url, data=metrics_message, headers=api_headers)
    http_response.raise_for_status()

    logger.info(
        f"Sent payload size={len(metrics_message)} encoding={api_headers.get('content-encoding', None)}"
    )
    return http_response.text


def handler(ctx: context.InvokeContext, data: io.BytesIO = None) -> response.Response:
    """
    Submits incoming metrics data to Datadog.

    Wraps incoming metrics data in a message payload and forwards this
    payload to a Datadog endpoint.

    Args:
      ctx:
        An fdk InvokeContext.
      data:
        A BytesIO stream containing a JSON representation of metrics.
        Each metric has the form:

    Returns:
      An fdk Response in which the body contains any error
      messages encountered during processing. At present, HTTP 200
      responses will always be returned.
    """

    try:
        serialized_metric_data = _get_serialized_metric_data(
            data,
        )
        

        metrics_message = _generate_metrics_msg(
            ctx,
            serialized_metric_data,
        )

        result = _send_metrics_msg_to_datadog(metrics_message)
    except HTTPError as e:
        logger.exception(f"Error sending metrics to Datadog")
        result = e.response.text
    except Exception as e:
        logger.exception("Unexpected error while processing input data")
        result = str(e)

    return response.Response(
        ctx,
        response_data=json.dumps({"result": result}),
        headers={"Content-Type": "application/json"},
    )