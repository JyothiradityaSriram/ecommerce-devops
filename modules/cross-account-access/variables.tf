
variable "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table in the data account"
  type        = string
}

variable "workload_role_arn" {
  description = "IAM role ARN from the EKS workload account"
  type        = string
}

variable "allowed_actions" {
  description = "DynamoDB actions permitted to the workload role"
  type        = list(string)

  default = [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:Query"
  ]
}

