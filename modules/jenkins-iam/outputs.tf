
output "role_arn" {
  value = aws_iam_role.jenkins.arn
}

output "instance_profile_name" {
  value = aws_iam_instance_profile.jenkins.name
}

output "ecr_policy_arn" {
  value = aws_iam_policy.ecr.arn
}

