resource "aws_lambda_function" "add_to_cart" {
  function_name = "addToCart"
  filename      = "addToCart.zip"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
}

resource "aws_lambda_function" "get_cart" {
  function_name = "getCart"
  filename      = "getCart.zip"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
}
