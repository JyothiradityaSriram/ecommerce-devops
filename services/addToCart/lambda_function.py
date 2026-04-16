import json
import boto3
import uuid
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cart')


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

        # ✅ Handle CORS
        if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return response(200, {})

        user_id = get_user_id(event)

        body = json.loads(event['body'])
        product_id = body['productId']
        quantity = body.get('quantity', 1)

        cart_id = str(uuid.uuid4())

        item = {
            'cartId': cart_id,
            'userId': user_id,
            'productId': product_id,
            'quantity': quantity,
            'createdAt': datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return response(200, {
            "message": "Item added to cart",
            "cartId": cart_id
        })

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return response(500, {"error": str(e)})
