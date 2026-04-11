import json
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

cart_table = dynamodb.Table("cart")
products_table = dynamodb.Table("Products")


def lambda_handler(event, context):
    try:
        logger.info(f"Incoming event: {event}")

        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        user_id = claims["sub"]

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
                logger.warning(f"Product missing: {item['productId']}")
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

        logger.info(f"Cart total: {cart_total}")

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "items": enriched_cart,
                "cartTotal": cart_total
            })
        }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
