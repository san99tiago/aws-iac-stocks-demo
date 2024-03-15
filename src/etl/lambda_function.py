# DEMO LAMBDA FUNCTION TO GET STOCK PRICE AND SAVE IT INTO DYNAMODB TABLE
# Copyright Santiago Garcia Arango

import os
import json
from datetime import datetime
import boto3
import yfinance as yf


STOCK_TICKER = os.environ["STOCK_TICKER"]
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
DYNAMODB_CLIENT = boto3.client("dynamodb")


def get_stock_price_from_ticker(ticker: str) -> float:
    """From a given Ticket (str), return the stock price."""
    stock = yf.Ticker("AMZN")
    stock_current_price = stock.info.get("currentPrice") or stock.info.get(
        "regularMarketPrice"
    )
    print(f"Retrieved stock_price for {ticker} is: {stock_current_price}")
    return stock_current_price


def save_stock_item_to_dynamodb(stock_ticker: str, stock_price: str):
    """Helper to save the DynamoDB item."""
    iso_datetime = datetime.now().isoformat()
    item = {
        "PK": {"S": f"TICKER#{stock_ticker}"},
        "SK": {"S": iso_datetime},
        "stock_ticker": {"S": stock_ticker},
        "stock_price ": {"S": str(stock_price)},
        "update_datetime": {"S": iso_datetime},
    }
    response = DYNAMODB_CLIENT.put_item(
        TableName=DYNAMODB_TABLE,
        Item=item,
    )
    print(response)
    return item


def lambda_handler(event, context):
    """Main entrypoint for the Lambda Function."""
    stock_price = get_stock_price_from_ticker(STOCK_TICKER)
    item = save_stock_item_to_dynamodb(STOCK_TICKER, stock_price)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item),
    }
