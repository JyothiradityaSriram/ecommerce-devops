
variable "name" {
  description = "Name prefix for network resources"
  type        = string
}

variable "aws_region" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

variable "enable_nat_gateway" {
  type    = bool
  default = true
}

variable "nat_gateway_count" {
  type    = number
  default = 1

  validation {
    condition     = var.nat_gateway_count >= 1 && var.nat_gateway_count <= length(var.availability_zones)
    error_message = "nat_gateway_count must be between 1 and the number of availability zones."
  }
}

variable "enable_interface_endpoints" {
  type    = bool
  default = true
}

