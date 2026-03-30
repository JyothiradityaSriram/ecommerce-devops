resource "aws_lambda_function" "backend" {
  function_name = "ecommerce-backend-${var.env}"

  filename      = "lambda.zip"
  handler       = "index.handler"
  runtime       = "python3.11"

  role = aws_iam_role.lambda_exec.arn
}
