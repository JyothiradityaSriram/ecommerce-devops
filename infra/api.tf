resource "aws_apigatewayv2_api" "api" {
  name          = "ecommerce-api"
  protocol_type = "HTTP"
}
