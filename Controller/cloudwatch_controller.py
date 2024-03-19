from datetime import datetime, timedelta
from Model.datapoint_model import DatapointModel


def get_ec2_stats(cloudwatch_client):
    response = cloudwatch_client.list_metrics(Namespace='AWS/EC2')
    return [metric['MetricName'] for metric in response['Metrics']]


def get_last_15_min_stats(metric_name, instance_id, cloudwatch_client):
    print(f"Metric: {metric_name} instance: {instance_id}")
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)

    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 60,  # The granularity in seconds (60 seconds for 1 minute)
                    'Stat': 'Average',  # change to other statistics like 'Sum', 'Maximum'...
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    print("Response metrics:")
    print(response['MetricDataResults'])
    return [
        DatapointModel(item[0], item[1]) for item in \
            list(zip(
                response['MetricDataResults'][0]['Timestamps'],
                response['MetricDataResults'][0]['Values'])
            )
        ]
