# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    Duration,
    Tags,
    aws_dynamodb,
    aws_lambda,
    aws_events,
    aws_events_targets,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct


class DemoStack(Stack):
    """
    Class to create the Demo Stack for the AWS resources via IaC with CDK in Python.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        """
        super().__init__(scope, construct_id, **kwargs)

        # Input parameters
        self.construct_id = construct_id
        self.stock_ticker = self.node.try_get_context("stock_ticker")

        # Main methods for the deployment
        self.create_dynamodb_table()
        self.create_lambda_layers()
        self.create_lambda_functions()
        self.configure_schedule_lambda_etl()
        self.generate_cloudformation_outputs()

    def create_dynamodb_table(self):
        """
        Create DynamoDB table for the NoSQL data.
        """
        self.dynamodb_table = aws_dynamodb.Table(
            self,
            "DynamoDB-Table",
            table_name=f"stock-prices-{self.construct_id}",
            partition_key=aws_dynamodb.Attribute(
                name="PK", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="SK", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        Tags.of(self.dynamodb_table).add("Name", f"stock-prices-{self.construct_id}")

    def create_lambda_layers(self) -> None:
        """
        Create the Lambda layers that are necessary for the additional runtime
        dependencies of the Lambda Functions.
        """

        # Layer for "yfinance" library to simplify fetching stock prices
        # -> Obtained from (https://github.com/san99tiago/aws-lambda-layers)
        self.lambda_layer_yfinance = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            "LambdaLayer-yfinance",
            layer_version_arn="arn:aws:lambda:us-east-1:226584130046:layer:python3-12-yfinance:1",
        )

    def create_lambda_functions(self) -> None:
        """
        Create the Lambda Functions for the solution.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_SRC_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
        )
        source_code_etl_path = os.path.join(PATH_TO_SRC_FOLDER, "etl")
        source_code_api_path = os.path.join(PATH_TO_SRC_FOLDER, "api")

        # ETL Lambda Function for updating the stock prices every 5 minutes
        self.lambda_stocks_etl: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-ETL-Stocks",
            function_name=f"stocks-etl-{self.construct_id}",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(source_code_etl_path),
            timeout=Duration.seconds(60),
            memory_size=512,
            environment={
                "DYNAMODB_TABLE": self.dynamodb_table.table_name,
                "STOCK_TICKER": self.stock_ticker,
            },
            layers=[
                self.lambda_layer_yfinance,
            ],
        )
        self.dynamodb_table.grant_read_write_data(self.lambda_stocks_etl)

        # API Lambda Function for exposing the stock prices via an API
        self.lambda_stocks_api: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-API-Stocks",
            function_name=f"stocks-api-{self.construct_id}",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(source_code_api_path),
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "DYNAMODB_TABLE": self.dynamodb_table.table_name,
                "STOCK_TICKER": self.stock_ticker,
            },
        )
        self.dynamodb_table.grant_read_write_data(self.lambda_stocks_api)

        # Exposing the Lambda function via a public URL
        # NOTE: If IAM-based based auth needed, update the "auth_type" to "AWS_IAM"
        self.lambda_function_url_stocks_api = self.lambda_stocks_api.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE
        )

    def configure_schedule_lambda_etl(self):
        """
        Method to create an automatic schedule to execute the Lambda Function ETL in a
        periodic fashion (eg: every 5 mins).
        """

        # Rule to enable the a schedule to run based on a CRON format or RATE expression
        self.event_rule_etl = aws_events.Rule(
            self,
            "EventBridge-Rule",
            enabled=True,
            rule_name=f"stocks-rule-{self.construct_id}",
            description=f"Event rule for scheduling {self.construct_id} ETL function periodically",
            schedule=aws_events.Schedule.rate(Duration.minutes(5)),
        )

        # Add Lambda function as a target for the Event Rule
        self.event_rule_etl.add_target(
            aws_events_targets.LambdaFunction(self.lambda_stocks_etl)
        )

    def generate_cloudformation_outputs(self):
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "LambdaFunctionUrl",
            value=self.lambda_function_url_stocks_api.url,
            description="URL to invoke the Lambda Function",
        )
