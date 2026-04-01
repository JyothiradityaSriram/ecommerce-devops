
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

orders_table = dynamodb.Table("Orders")
order_items_table = dynamodb.Table("OrderItems")

def lambda_handler(event, context):

    try:
        claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        user_id = claims["sub"]

        response = orders_table.query(
            IndexName="userId-index",
            KeyConditionExpression=Key("userId").eq(user_id)
        )

        orders = response["Items"]

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

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
