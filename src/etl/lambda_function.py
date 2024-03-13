# DEMO LAMBDA FUNCTION TO GET STOCK PRICE AND SAVE IT INTO DYNAMODB TABLE
# Copyright Santiago Garcia Arango

import json
from datetime import datetime
import yfinance as yf


def get_stock_price_from_ticker(ticker: str) -> float:
    """From a given Ticket (str), return the stock price."""
    stock = yf.Ticker("AMZN")
    stock_current_price = stock.info.get("currentPrice") or stock.info.get(
        "regularMarketPrice"
    )
    print(f"Retrieved stock_price for {ticker} is: {stock_current_price}")
    return stock_current_price


def lambda_handler(event, context):
    """Main entrypoint for the Lambda Function."""

    # TODO: make dynamic ticker from event or env-vars
    ticker = "AMZN"
    price = get_stock_price_from_ticker(ticker)

    # TODO: Add save to DynamoDB Table action for the demo

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "Stocks": [
                    {
                        "stock_name": "Amazon.com",
                        "ticker": ticker,
                        "stock_price ": price,
                        "update_datetime": datetime.now().isoformat(),
                    }
                ]
            }
        ),
    }
