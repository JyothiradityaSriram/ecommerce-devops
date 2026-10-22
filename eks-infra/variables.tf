variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "cluster_name" {
  type    = string
  default = "ecommerce-eks"
}
variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["ap-south-1a", "ap-south-1b"]
}

variable "enable_nat_gateway" {
  description = "Create a NAT Gateway for private subnet internet egress"
  type        = bool
  default     = true
}

variable "enable_interface_endpoints" {
  description = "Create selected AWS interface VPC endpoints"
  type        = bool
  default     = true
}

variable "eks_version" {
  type    = string
  default = "1.34"
}

variable "node_instance_types" {
  type    = list(string)
  default = ["t3.small"]
}

variable "node_desired_size" {
  type    = number
  default = 1
}

variable "node_min_size" {
  type    = number
  default = 1
}

variable "node_max_size" {
  type    = number
  default = 2
}
variable "nat_gateway_count" {
  description = "Number of NAT gateways to create when enabled"
  type        = number
  default     = 1

  validation {
    condition     = var.nat_gateway_count >= 1 && var.nat_gateway_count <= length(var.availability_zones)
    error_message = "nat_gateway_count must be between 1 and the number of availability zones."
  }
}
