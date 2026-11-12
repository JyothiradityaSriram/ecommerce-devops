
import json
import math
import sys
from pathlib import Path

REQUIRED_FIELDS = {
    "product_id",
    "product_name",
    "price",
    "category",
}


def validate_product(product):
    if not isinstance(product, dict):
        return ["Product must be a JSON object"]

    errors = []

    missing_fields = REQUIRED_FIELDS - product.keys()

    if missing_fields:
        errors.append(f"Missing fields: {sorted(missing_fields)}")

    for field in REQUIRED_FIELDS.intersection(product.keys()):
        value = product[field]

        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"Field '{field}' cannot be empty")

    if "price" in product:
        price = product["price"]

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            errors.append("Price must be a number")
        elif not math.isfinite(price) or price < 0:
            errors.append("Price must be a finite, non-negative number")

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <json-file>")
        return 2

    file_path = Path(sys.argv[1])

    try:
        with file_path.open(encoding="utf-8") as file:
            products = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to read valid JSON: {error}")
        return 2

    if isinstance(products, dict):
        products = [products]

    if not isinstance(products, list) or not products:
        print("Validation failed: expected a non-empty JSON object or array")
        return 1

    failed = False

    for index, product in enumerate(products, start=1):
        errors = validate_product(product)

        if errors:
            failed = True
            for error in errors:
                print(f"Record {index}: {error}")

    if failed:
        print("Data validation FAILED")
        return 1

    print(f"Data validation PASSED: {len(products)} product(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

