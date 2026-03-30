resource "aws_cognito_user_pool_client" "userpool_client" {
  name         = "client"
  user_pool_id = aws_cognito_user_pool.pool.id

  generate_secret = false

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]

  allowed_oauth_scopes = ["email", "openid", "profile"]

  supported_identity_providers = ["COGNITO"]

  callback_urls = [
    "https://example.com/callback"
  ]

  default_redirect_uri = "https://example.com/callback"

  logout_urls = [
    "https://example.com/logout"
  ]

  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }

  access_token_validity  = 60
  id_token_validity      = 60
  refresh_token_validity = 30
}
