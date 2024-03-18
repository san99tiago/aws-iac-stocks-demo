# 📈 AWS-IAC-STOCKS-DEMO 📈

<img src="assets/aws_iac_stocks_demo.png" width=80%> <br>

## Overview 🔮

This is an IaC Demo with that contains an API and ETL that process Stock Prices deployed on AWS with the following specifications:

- Infrastructure as Code with [AWS CDK-Python](https://aws.amazon.com/cdk/) or [Terraform](https://www.terraform.io)
- Source Code with [AWS Lambda Functions](https://aws.amazon.com/lambda/) built with [Python Runtime](https://www.python.org)
- ETL that downloads stock prices with [yfinance](https://pypi.org/project/yfinance/) (Yahoo Finance's API)
- [DynamoDB](https://aws.amazon.com/dynamodb/) as the NoSQL database for saving the stock prices
- Python dependencies managed by [requirements.txt](./requirements.txt)
- Tests with [PyTest Framework](https://docs.pytest.org/)

## How to run this project? :dizzy:

### Deployment

(Optional) Login to your AWS Account, and go to the "[Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home?region=us-east-1#/)" service. Then proceed to "create an environment", and use these settings (default):

- Name: _Choose the preferred name_
- Environment type: New EC2 instance
- Instance type: t2.micro (1 GiB RAM + 1 vCPU)
- Platform: Amazon Linux 2023
- Timeout: 30 minutes
- Connection: AWS Systems Manager (SSM)

Now, wait for the environment to be ready, select it, and click on "Open in Cloud9" to access it.

Once in your Cloud9 environment, you can proceed to clone the repository as follows:

```bash
git clone https://github.com/san99tiago/aws-iac-stocks-demo
cd aws-iac-stocks-demo
```

Proceed to install the Python dependencies:

```bash
pip install -r requirements.txt
```

To deploy the solution (with the help of [Cloud Development Kit](https://aws.amazon.com/cdk/)), you can run:

```bash
cdk deploy
# Approve (press "y")
```

| This command will create a CloudFormation Stack that contains the Infrastructure as Code for the necessary AWS resources.

### What is going on now?

- First, you can go to "CloudFormation" service, and search for the stack. Inside the stack, in the "Resources" tab, you will find:

  - DynamoDB-Table: NoSQL Database that will store the Stock prices over time.
  - EventBridge-Rule: Enables to periodically run the ETL (eg: every 5 minutes).
  - Lambda-ETL-Stocks: Runtime for the Extract-Transform-Load logic to fetch and save the stock prices periodically.
  - Lambda-API-Stocks: Runtime for the API that exposes the latest stock prices.

<img src="assets/aws_iac_stocks_demo_stack.png" width=60%> <br>

- Second, you can go to "DynamoDB", and check the DynamoDB table that has a prefix `stock-prices-stocks-demo-***`, and click on "Explore Table Items", to see how the data gets loaded to the table as items with datetime and additional attributes.

<img src="assets/aws_iac_stocks_demo_dynamodb.png" width=60%> <br>

- Finally, you can use the `LambdaFunctionUrl` (that is the generated Output in the CloudFormation Stack), to execute the API that is able to get the latest stock prices from the DynamoDB table and return them in a specific format ready to be used by other consumers/users/systems.

<img src="assets/aws_iac_stocks_demo_api.png" width=60%> <br>

### Destroy (To avoid costs)

To destroy/remove the resources, run:

```bash
cdk destroy
# Approve (press "y")
```

## Special thanks 🎁

- Thanks to all contributors of the great OpenSource projects that I am using. <br>

## Author 🎹

### Santiago Garcia Arango

<table border="1">
    <tr>
        <td>
            <p align="center">Curious DevOps Engineer passionate about advanced cloud-based solutions and deployments in AWS. I am convinced that today's greatest challenges must be solved by people that love what they do.</p>
        </td>
        <td>
            <p align="center"><img src="assets/SantiagoGarciaArango_AWS.png" width=80%></p>
        </td>
    </tr>
</table>

## LICENSE

Copyright 2024 Santiago Garcia Arango.
