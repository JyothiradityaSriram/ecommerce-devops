resource "aws_cloudwatch_log_group" "cart_logs" {
  name              = "/ecs/cart-service"
  retention_in_days = 14
}
