import subprocess
import boto3


def check_aws_configuration():
    client = boto3.client('s3')

    if client is None:
        raise ValueError("boto3 client is None")

    output = subprocess.check_output('aws configure list | grep profile | grep "<not set>" | wc -l', shell=True)
    if int(output.decode("utf-8")) == 1:
        raise ValueError("No profile is set as default")


def get_session(profile='default'):
    return boto3.Session(profile_name=profile)