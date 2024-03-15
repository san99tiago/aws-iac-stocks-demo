# DEMO LAMBDA FUNCTION TO GET LATEST STOCK PRICES FROM DYNAMODB AND EXPOSE THEM
# Copyright Santiago Garcia Arango

import os
import json
import boto3

STOCKS_LIMIT = 10
STOCK_TICKER = os.environ["STOCK_TICKER"]
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
DYNAMODB_CLIENT = boto3.client("dynamodb")


def get_latest_stock_items_from_dynamodb():
    """Helper to get the latest stock items from DynamoDB"""
    response = DYNAMODB_CLIENT.query(
        TableName=DYNAMODB_TABLE,
        KeyConditions={
            "PK": {
                "AttributeValueList": [{"S": f"TICKER#{STOCK_TICKER}"}],
                "ComparisonOperator": "EQ",
            }
        },
        ScanIndexForward=False,
        Limit=STOCKS_LIMIT,
    )
    print(f"Response from query for ticker: {STOCK_TICKER}")
    print(response)

    if "Items" in response:
        stocks = response["Items"]
        # Transform items to desired format using list comprehension
        transformed_stocks = [
            {
                "update_datetime": item["update_datetime"]["S"],
                "stock_ticker": item["stock_ticker"]["S"],
                "stock_price ": item["stock_price "]["S"],
            }
            for item in stocks
        ]
        return transformed_stocks
    else:
        return []


def lambda_handler(event, context):
    """Main entrypoint for the Lambda Function."""

    items = get_latest_stock_items_from_dynamodb()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }
