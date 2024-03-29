from Model.ec2_model import EC2Model


def get_ec2_regions(ec2_client):
    regions = ec2_client.describe_regions()['Regions']
    return [region['RegionName'] for region in regions]


def get_subnets(ec2_client):
    response = ec2_client.describe_subnets()
    return [subnet['SubnetId'] for subnet in response['Subnets']]


def get_security_groups(ec2_client):
    response = ec2_client.describe_security_groups()
    return [sg['GroupId'] for sg in response['SecurityGroups']]


def get_key_pairs(ec2_client):
    response = ec2_client.describe_key_pairs()
    return [key_pair['KeyName'] for key_pair in response['KeyPairs']]


def find_ubuntu_ami(ec2_client):
    filters = [
        {'Name': 'virtualization-type', 'Values': ['hvm']},
        {'Name': 'architecture', 'Values': ['x86_64']},
        {'Name': 'owner-id', 'Values': ['099720109477']},
    ]
    response = ec2_client.describe_images(Filters=filters)
    latest_ami_id = response['Images'][0]['ImageId']
    return latest_ami_id


def run_ec2_instance(ec2_client, image_id, instance_type, key_name, security_group_ids,
                     subnet_id, min_count=1, max_count=1):
    response = ec2_client.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=min_count,
        MaxCount=max_count,
        SecurityGroupIds=security_group_ids,
        SubnetId=subnet_id
    )

    instance_ids = [instance['InstanceId'] for instance in response['Instances']]
    print(f"Instances launched successfully: {', '.join(instance_ids)}")
    return instance_ids


def get_running_instances(ec2_client, instance_ids):
    response = ec2_client.describe_instances(InstanceIds=instance_ids)

    instances = response['Reservations']
    if instances:
        print("Running Instances:")
        instance_ids = []
        for reservation in instances:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                print(f"Instance ID: {instance_id}, State: {state}")
                instance_ids.append(instance_id)

        return instance_ids
    else:
        print("No running instances found.")
        return []


def get_ec2_instances(ec2_client):
    response = ec2_client.describe_instances()

    result = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            result.append(EC2Model(instance['InstanceId'], instance['State']['Name']))

    return result


def stop_ec2_instance(ec2_client, instance_id):
    ec2_client.stop_instances(InstanceIds=[instance_id])
