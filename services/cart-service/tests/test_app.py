
import jwt
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def make_token(user_id="test-user", secret=None):
    import app as cart_app

    if secret is None:
        secret = cart_app.JWT_SECRET

    return jwt.encode(
        {"sub": user_id},
        secret,
        algorithm="HS256",
    )

def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_cart_without_token_returns_401(client):
    response = client.get("/cart")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Token is missing"


def test_cart_with_invalid_token_returns_401(client):
    response = client.get(
        "/cart",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid token"


def test_add_cart_without_product_id_returns_400(client, monkeypatch):
    import app as cart_app

    monkeypatch.setattr(
        cart_app.table,
        "update_item",
        lambda **kwargs: pytest.fail("DynamoDB should not be called"),
    )

    response = client.post(
        "/cart",
        json={"quantity": 1},
        headers={"Authorization": f"Bearer {make_token()}"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "productId required"


def test_get_cart_returns_items(client, monkeypatch):
    import app as cart_app

    def fake_query(**kwargs):
        assert kwargs["KeyConditionExpression"] is not None
        return {
            "Items": [
                {"userId": "test-user", "productId": "product-1", "quantity": 2}
            ]
        }

    monkeypatch.setattr(cart_app.table, "query", fake_query)

    response = client.get(
        "/cart",
        headers={"Authorization": f"Bearer {make_token()}"},
    )

    assert response.status_code == 200
    assert response.get_json()["cart"][0]["productId"] == "product-1"
