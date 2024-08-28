import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.stop_instances(
        InstanceIds=['instance-id'],
    )
    print(f'Stopped EC2 instances: {response}')
