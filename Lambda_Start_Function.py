import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.start_instances(
        InstanceIds=['instance-id'],
    )
    print(f'Started EC2 instances: {response}')
