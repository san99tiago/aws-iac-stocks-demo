# DEMO LAMBDA FUNCTION TO EXPOSE STOCK DATA FROM A DYNAMODB TABLE
# Copyright Santiago Garcia Arango

import json
from datetime import datetime


def lambda_handler(event, context):
    """Main entrypoint for the Lambda Function."""

    # TODO: Add READ to DynamoDB Table action for the demo

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "Stocks": [
                    {
                        "stock_name": "TBD",
                        "ticker": "TBD",
                        "stock_price ": "TBD",
                        "update_datetime": "TBD",
                    }
                ]
            }
        ),
    }
