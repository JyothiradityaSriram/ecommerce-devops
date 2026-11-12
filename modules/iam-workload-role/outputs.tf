
output "role_arn" {
  value = aws_iam_role.workload.arn
}

output "policy_arn" {
  value = aws_iam_policy.dynamodb_access.arn
}

