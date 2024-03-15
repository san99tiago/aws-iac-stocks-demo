# DEMO LAMBDA FUNCTION TO EXPOSE STOCK DATA FROM A DYNAMODB TABLE
# Copyright Santiago Garcia Arango

import os
import json
from datetime import datetime
import boto3


STOCK_TICKER = os.environ["STOCK_TICKER"]
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
DYNAMODB_CLIENT = boto3.client("dynamodb")


def get_latest_stock_items_from_dynamodb():
    """Helper to get the latest stock items from DynamoDB"""
    # TODO: Add real dynamodb operation(s)
    items = [{"item1", "item2", "item3", "item4", "item5"}]
    return items


def lambda_handler(event, context):
    """Main entrypoint for the Lambda Function."""

    items = get_latest_stock_items_from_dynamodb()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }
