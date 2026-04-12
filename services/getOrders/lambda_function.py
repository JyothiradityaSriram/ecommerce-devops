import json
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

orders_table = dynamodb.Table("Orders")
order_items_table = dynamodb.Table("OrderItems")


def lambda_handler(event, context):
    try:
        logger.info(f"Incoming event: {event}")

        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        user_id = claims["sub"]

        logger.info(f"User ID: {user_id}")

        response = orders_table.query(
            IndexName="userId-index",
            KeyConditionExpression=Key("userId").eq(user_id)
        )

        orders = response["Items"]

        logger.info(f"Orders fetched: {len(orders)}")

        result = []

        for o in orders:
            logger.info(f"Processing order: {o['orderId']}")

            items_response = order_items_table.query(
                KeyConditionExpression=Key("orderId").eq(o["orderId"])
            )

            result.append({
                "orderId": o["orderId"],
                "total": o["total"],
                "createdAt": o["createdAt"],
                "items": items_response["Items"]
            })

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(result)
        }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
