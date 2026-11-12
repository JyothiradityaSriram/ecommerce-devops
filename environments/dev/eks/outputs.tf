
output "vpc_id" {
  description = "DEV VPC ID"
  value       = module.network.vpc_id
}

output "public_subnet_ids" {
  description = "DEV public subnet IDs"
  value       = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  description = "DEV private subnet IDs"
  value       = module.network.private_subnet_ids
}

output "nat_gateway_ids" {
  description = "DEV NAT Gateway IDs"
  value       = module.network.nat_gateway_ids
}
output "cart_workload_role_arn" {
  value = module.cart_workload_role.role_arn
}
