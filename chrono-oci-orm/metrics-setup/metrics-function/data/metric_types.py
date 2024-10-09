import json

with open('metric_types.json', 'r') as f:
    metrics = json.load(f)

def modify_metric_type(metrics):
    for key, value in metrics.items():
        if 'aggregationTemporality' in value:
            if value['aggregationTemporality'] == 1:
                value['metric_type'] = "delta_counter"
            if value['aggregationTemporality'] == 2:
                value['metric_type'] = "cumulative_counter"  
            
            del value['aggregationTemporality']
    return metrics

modified_data = modify_metric_type(metrics)

with open('metric_types.json', 'w') as f:
    json.dump(modified_data, f, indent=4)


            