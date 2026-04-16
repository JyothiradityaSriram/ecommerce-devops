import json
import boto3
from decimal import Decimal
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Products")


def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(body, default=convert_decimal)
    }


def lambda_handler(event, context):
    try:
        if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return response(200, {})

        result = table.scan()

        return response(200, result.get("Items", []))

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response(500, {"error": str(e)})
