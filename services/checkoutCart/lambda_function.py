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


def lambda_handler(event, context):
    try:
        logger.info(f"Incoming event: {event}")

        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        user_id = claims["sub"]

        cart = cart_table.query(
            KeyConditionExpression=Key("userId").eq(user_id)
        )["Items"]

        logger.info(f"Cart items: {cart}")

        if not cart:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"message": "Cart is empty"})
            }

        items = []
        total = 0

        for c in cart:
            product_response = products_table.get_item(
                Key={"id": c["productId"]}
            )

            if "Item" not in product_response:
                logger.warning(f"Product not found: {c['productId']}")
                continue

            product = product_response["Item"]

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

        logger.info(f"Order created: {order_id}, total: {total}")

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

        # Clear cart
        for c in cart:
            cart_table.delete_item(
                Key={
                    "userId": user_id,
                    "productId": c["productId"]
                }
            )

        logger.info("Cart cleared")

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "message": "Order placed",
                "orderId": order_id
            })
        }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
