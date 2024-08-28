# Automating EC2 Start/Stop with Lambda and CloudWatch

## Introduction

This project automates the starting and stopping of EC2 instances using AWS Lambda and CloudWatch. We will create two Lambda functions: one to start the instances and another to stop them, triggered by CloudWatch EventBridge on a defined schedule.

## Prerequisites

- An AWS account with administrative access.
- Basic understanding of IAM, Lambda, and EC2.

## Step-by-Step Instructions

### 1. Creating IAM Policies and Roles

#### a. **Create IAM Policy for Starting Instances**
1. Navigate to the **IAM** console in AWS.
2. Go to **Policies** and click **Create policy**.
3. Choose the **JSON** tab and enter the following code:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "ec2:StartInstances",
                "Resource": "arn:aws:ec2:region:account-id:instance/instance-id"
            }
        ]
    }
    ```
4. Review and name the policy `EC2StartPolicy`.

#### b. **Create IAM Policy for Stopping Instances**
1. Follow the same steps as above, but use this JSON:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "ec2:StopInstances",
                "Resource": "arn:aws:ec2:region:account-id:instance/instance-id"
            }
        ]
    }
    ```
2. Name this policy `EC2StopPolicy`.

#### c. **Create IAM Roles**
1. Go to **Roles** and click **Create role**.
2. Choose **AWS service** and select **Lambda**.
3. Attach the `EC2StartPolicy` to the role. Name the role `LambdaEC2StartRole`.
4. Repeat the process for `EC2StopPolicy`, naming the role `LambdaEC2StopRole`.

### 2. Lambda Functions

#### a. **Create the StartEC2 Function**
1. Navigate to the **Lambda** console and click **Create function**.
2. Choose **Author from scratch**, name the function `StartEC2`.
3. Choose Python 3.x as the runtime.
4. Attach the `LambdaEC2StartRole` created earlier.
5. In the code editor, replace the existing code with the following:

    ```python
    import boto3

    def lambda_handler(event, context):
        ec2 = boto3.client('ec2')
        response = ec2.start_instances(
            InstanceIds=['instance-id'],
        )
        print(f'Started EC2 instances: {response}')
    ```

6. Click **Deploy**.

#### b. **Create the StopEC2 Function**
1. Repeat the steps above, but name the function `StopEC2`.
2. Attach the `LambdaEC2StopRole`.
3. Replace the code with:

    ```python
    import boto3

    def lambda_handler(event, context):
        ec2 = boto3.client('ec2')
        response = ec2.stop_instances(
            InstanceIds=['instance-id'],
        )
        print(f'Stopped EC2 instances: {response}')
    ```

4. Click **Deploy**.

### 3. Setting Up CloudWatch EventBridge Rules

#### a. **Create a Rule for Starting Instances**
1. Navigate to the **CloudWatch** console and go to **Rules** under **Events**.
2. Click **Create rule**.
3. Under **Event Source**, choose **EventBridge (CloudWatch Events)** and select **Schedule**.
4. Define the schedule using a cron expression, e.g., `cron(0 8 * * ? *)` for 8 AM UTC every day.
5. Choose the `StartEC2` Lambda function as the target.
6. Click **Create**.

#### b. **Create a Rule for Stopping Instances**
1. Repeat the steps above, but use a different cron expression, e.g., `cron(0 20 * * ? *)` for 8 PM UTC every day.
2. Choose the `StopEC2` Lambda function as the target.
3. Click **Create**.

### 4. Testing and Validation

#### a. **Manual Testing**
1. Go to the **Lambda** console and select `StartEC2`.
2. Click **Test** and create a new test event. The EC2 instance should start.
3. Repeat the process with `StopEC2` to stop the instance.

#### b. **Scheduled Testing**
1. Wait for the scheduled time or adjust the cron expression for testing purposes.
2. Verify that the EC2 instance starts and stops according to the schedule.

## Conclusion

This project demonstrates how to automate EC2 instance management using Lambda and CloudWatch. You can expand on this by adding more instances, custom schedules, or additional AWS services.

