# Pyside_AWS_boto3_app

Simple application to control AWS VMs & S3 buckets using the MVC design pattern.


Uses Python, boto3 (for AWS) and PySide2

## Configure AWS CLI

1. Download and install AWS cli (follow the website instructions: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Create an IAM account with EC2 FullAccess, S3 FullAccess & CloudWatch ReadAccess
3. Create access keys and insert them into the CLI with aws configure
4. On ~/.aws/config check that the user is set as default first (like in the example)
```toml
[default]
region = eu-west-3
output = json
```
5. Check ~/.aws/credentials that the user is default with:
```toml
[default]
aws_access_key_id=...
aws_secret_access_key=...
```
6. Check with aws configure list
7. If default is not the user you see on the command, modify ~/.bashrc with:
```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=eu-west-3
export AWS_DEFAULT_PROFILE=default
export AWS_PROFILE=default
```
8. Run source ~/.bashrc and check again aws configure list

> Replace the ... in every example with your keys


## Run

```bash
python3 main.py
```


