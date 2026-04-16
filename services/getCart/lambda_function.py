import json
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

cart_table = dynamodb.Table("cart")
products_table = dynamodb.Table("Products")


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

        cart_response = cart_table.query(
            KeyConditionExpression=Key("userId").eq(user_id)
        )

        cart_items = cart_response.get("Items", [])

        enriched_cart = []
        cart_total = 0

        for item in cart_items:
            product_response = products_table.get_item(
                Key={"id": item["productId"]}
            )

            if "Item" not in product_response:
                continue

            product = product_response["Item"]

            price = int(product["price"])
            quantity = int(item["quantity"])
            subtotal = price * quantity

            enriched_cart.append({
                "productId": item["productId"],
                "name": product["name"],
                "price": price,
                "quantity": quantity,
                "subtotal": subtotal
            })

            cart_total += subtotal

        return response(200, {
            "items": enriched_cart,
            "cartTotal": cart_total
        })

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response(500, {"error": str(e)})
