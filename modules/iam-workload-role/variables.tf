
variable "aws_region" {
  type = string
}
variable "role_name" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "namespace" {
  type    = string
  default = "default"
}

variable "service_account_name" {
  type    = string
  default = "cart-service-sa"
}

variable "dynamodb_table_arn" {
  type = string
}

