resource "aws_secretsmanager_secret" "jwt" {
  name = "cart-service/jwt-secret"
}
