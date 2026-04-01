import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cart-table')  # your DynamoDB table name

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        user_id = body['userId']
        product_id = body['productId']
        quantity = body['quantity']

        cart_id = str(uuid.uuid4())

        item = {
            'cartId': cart_id,
            'userId': user_id,
            'productId': product_id,
            'quantity': quantity,
            'createdAt': datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item added to cart",
                "cartId": cart_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
