from Model.bucket_model import BucketModel
from Model.object_model import ObjectModel


def get_available_regions():
    # TODO: change for code. get_available_regions returns also disabled regions
    return [
        "ap-northeast-1",
        "ap-northeast-2",
        "ap-northeast-3",
        "ap-south-1",
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "ca-central-1",
        "sa-east-1",
        "eu-north-1",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "eu-central-1"
    ]


def get_buckets(s3_client):
    response = s3_client.list_buckets()
    return [BucketModel(bucket['Name']) for bucket in response['Buckets']]


def create_bucket(s3_client, bucket_name, region):
    s3_client.create_bucket(Bucket=bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': region})


def delete_bucket(s3_client, bucket_name):
    bucket = s3_client.Bucket(bucket_name)
    bucket.delete()


def get_bucket_objects(s3_client, bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    return [ObjectModel(obj['Key'], obj['Size']) for obj in response.get('Contents', [])]


def upload_object(s3_client, bucket_name, object_key, file_path):
    s3_client.upload_file(file_path, bucket_name, object_key)
    print(f"Object '{object_key}' uploaded successfully to bucket '{bucket_name}'.")


def delete_object(s3_client, bucket_name, object_key):
    s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    print(f"Object '{object_key}' deleted successfully from bucket '{bucket_name}'.")