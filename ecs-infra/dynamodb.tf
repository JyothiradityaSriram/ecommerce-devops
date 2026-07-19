
resource "aws_dynamodb_table" "cart" {
  name         = "cart"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "userId"
  range_key = "productId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "productId"
    type = "S"
  }

  tags = {
    Name = "cart-table"
  }
}
