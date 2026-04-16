import json
import boto3
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

cart_table = dynamodb.Table("cart")
products_table = dynamodb.Table("Products")
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

        cart = cart_table.query(
            KeyConditionExpression=Key("userId").eq(user_id)
        )["Items"]

        if not cart:
            return response(400, {"message": "Cart is empty"})

        items = []
        total = 0

        for c in cart:
            product = products_table.get_item(
                Key={"id": c["productId"]}
            ).get("Item")

            if not product:
                continue

            price = int(product["price"])
            quantity = int(c["quantity"])
            subtotal = price * quantity

            items.append({
                "productId": c["productId"],
                "name": product["name"],
                "price": price,
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

        order_id = str(uuid.uuid4())

        orders_table.put_item(
            Item={
                "orderId": order_id,
                "userId": user_id,
                "total": total,
                "createdAt": datetime.utcnow().isoformat()
            }
        )

        for i in items:
            order_items_table.put_item(
                Item={
                    "orderId": order_id,
                    "productId": i["productId"],
                    "quantity": i["quantity"],
                    "price": i["price"],
                    "subtotal": i["subtotal"]
                }
            )

        # clear cart
        for c in cart:
            cart_table.delete_item(
                Key={
                    "userId": user_id,
                    "productId": c["productId"]
                }
            )

        return response(200, {
            "message": "Order placed",
            "orderId": order_id
        })

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response(500, {"error": str(e)})
