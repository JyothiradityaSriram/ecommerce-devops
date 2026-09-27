output "alb_url" {
  value = aws_lb.alb.dns_name
}

output "jwt_secret_arn" {
  value = aws_secretsmanager_secret.jwt.arn
}
