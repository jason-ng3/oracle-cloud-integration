import os
import re

def get_metric_name(log_record: dict):
    """
    :return: Metric name in the form of oci_<namespace>_<metric_name>
    """

    elements = get_dictionary_value(log_record, 'namespace').split('_')
    elements += camel_case_split(get_dictionary_value(log_record, 'name'))
    elements = [element.lower() for element in elements]
    return '.'.join(elements)

def camel_case_split(str):
    """Splits camel case string to individual strings"""
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)

def get_metric_points(log_record: dict):
    result = []

    datapoints = get_dictionary_value(dictionary=log_record, target_key='datapoints')
    for datapoint in datapoints:
        # Calculate required TimeUnixNano
        unix_timestamp_nano_str = str(int(datapoint.get('timestamp')) * 1_000_000)

        converted_datapoint = {'asDouble': datapoint.get('value'),
                    'timeUnixNano': unix_timestamp_nano_str}

        result.append(converted_datapointpoint)

    return result

def get_dictionary_value(dictionary: dict, target_key: str):
    """
    Recursively locate value within nested dictionary
    :return: First target_key found
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
    return os.environ.get("CHRONO_COMPRESS", "false").lower() == "true"