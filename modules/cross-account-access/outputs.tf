
output "resource_policy_id" {
  value = aws_dynamodb_resource_policy.cross_account.id
}

output "resource_policy" {
  value = aws_dynamodb_resource_policy.cross_account.policy
}

