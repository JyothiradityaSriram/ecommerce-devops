import os
import logging
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key
import jwt

# ---------- CONFIG ----------
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
TABLE_NAME = os.getenv("CART_TABLE", "cart")

# JWT Secret (store in env variable in real production)
JWT_SECRET = os.getenv("JWT_SECRET", "my-super-secret-key")
JWT_ALGORITHM = "HS256"

# ---------- APP SETUP ----------
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# ---------- AWS SETUP ----------
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)


# ---------- JWT AUTH HELPER ----------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Expecting:
        # Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded_jwt = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )

            # JWT standard claim:
            # sub = subject = user identity
            user_id = decoded_jwt["sub"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        except Exception:
            logging.exception("JWT validation failed")
            return jsonify({"error": "Authentication failed"}), 401

        return f(user_id, *args, **kwargs)

    return decorated


# ---------- ADD / UPDATE CART ----------
@app.route("/cart", methods=["POST"])
@token_required
def add_to_cart(user_id):
    try:
        data = request.json

        product_id = data.get("productId")
        quantity = int(data.get("quantity", 1))

        if not product_id:
            return jsonify({"error": "productId required"}), 400

        table.update_item(
            Key={
                "userId": user_id,
                "productId": product_id
            },
            UpdateExpression="""
                SET quantity = if_not_exists(quantity, :zero) + :q
            """,
            ExpressionAttributeValues={
                ":q": quantity,
                ":zero": 0
            }
        )

        return jsonify({"message": "Cart updated"}), 200

    except Exception:
        logging.exception("Error adding to cart")
        return jsonify({"error": "Internal server error"}), 500


# ---------- GET CART ----------
@app.route("/cart", methods=["GET"])
@token_required
def get_cart(user_id):
    try:
        items = []
        last_evaluated_key = None

        while True:
            query_params = {
                "KeyConditionExpression": Key("userId").eq(user_id)
            }

            if last_evaluated_key:
                query_params["ExclusiveStartKey"] = last_evaluated_key

            response = table.query(**query_params)

            items.extend(response.get("Items", []))

            last_evaluated_key = response.get("LastEvaluatedKey")

            if not last_evaluated_key:
                break

        return jsonify({"cart": items}), 200

    except Exception:
        logging.exception("Error fetching cart")
        return jsonify({"error": "Internal server error"}), 500


# ---------- REMOVE ITEM ----------
@app.route("/cart", methods=["DELETE"])
@token_required
def remove_from_cart(user_id):
    try:
        data = request.json

        product_id = data.get("productId")

        if not product_id:
            return jsonify({"error": "productId required"}), 400

        table.delete_item(
            Key={
                "userId": user_id,
                "productId": product_id
            }
        )

        return jsonify({"message": "Item removed"}), 200

    except Exception:
        logging.exception("Error removing item")
        return jsonify({"error": "Internal server error"}), 500


# ---------- HEALTH CHECK ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ---------- OPTIONAL: TEST TOKEN GENERATOR ----------
@app.route("/generate-token", methods=["GET"])
def generate_token():
    """
    ONLY for local testing.
    Remove in production.
    """

    token = jwt.encode(
        {
            "sub": "user-123",
            "email": "test@example.com"
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return jsonify({
        "token": token
    })


# ---------- ENTRY ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)