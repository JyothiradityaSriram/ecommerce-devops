resource "random_password" "jwt" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "jwt" {
  name = "cart-service/jwt-secret"
}

resource "aws_secretsmanager_secret_version" "jwt" {
  secret_id = aws_secretsmanager_secret.jwt.id

  secret_string = jsonencode({
    JWT_SECRET = random_password.jwt.result
  })
}
