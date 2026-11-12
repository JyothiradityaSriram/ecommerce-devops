
import pytest
from validate_data import validate_product


def valid_product():
    return {
        "product_id": "P101",
        "product_name": "Laptop",
        "price": 50000,
        "category": "Electronics",
    }


def test_valid_product():
    product = valid_product()

    assert validate_product(product) == []


def test_missing_product_id():
    product = valid_product()
    del product["product_id"]

    errors = validate_product(product)

    assert any("product_id" in error for error in errors)


def test_empty_product_name():
    product = valid_product()
    product["product_name"] = ""

    errors = validate_product(product)

    assert any("product_name" in error for error in errors)


def test_negative_price():
    product = valid_product()
    product["price"] = -100

    errors = validate_product(product)

    assert any("non-negative" in error for error in errors)


def test_string_price():
    product = valid_product()
    product["price"] = "50000"

    errors = validate_product(product)

    assert any("Price must be a number" in error for error in errors)


@pytest.mark.parametrize("price", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_price(price):
    product = valid_product()
    product["price"] = price

    errors = validate_product(product)

    assert any("non-negative" in error for error in errors)


def test_product_must_be_dictionary():
    errors = validate_product("invalid product")

    assert "Product must be a JSON object" in errors


def test_missing_multiple_fields():
    product = {"price": 100}

    errors = validate_product(product)

    assert any("Missing fields" in error for error in errors)

