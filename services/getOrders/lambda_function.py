import json
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

orders_table = dynamodb.Table("Orders")
order_items_table = dynamodb.Table("OrderItems")


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS"
        },
        "body": json.dumps(body)
    }


def get_user_id(event):
    return event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]


def lambda_handler(event, context):
    try:
        logger.info(f"Incoming event: {event}")

        if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return response(200, {})

        user_id = get_user_id(event)

        response_db = orders_table.query(
            IndexName="userId-index",
            KeyConditionExpression=Key("userId").eq(user_id)
        )

        orders = response_db["Items"]

        result = []

        for o in orders:
            items_response = order_items_table.query(
                KeyConditionExpression=Key("orderId").eq(o["orderId"])
            )

            result.append({
                "orderId": o["orderId"],
                "total": o["total"],
                "createdAt": o["createdAt"],
                "items": items_response["Items"]
            })

        return response(200, result)

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response(500, {"error": str(e)})
