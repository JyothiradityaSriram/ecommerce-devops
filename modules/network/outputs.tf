
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "public_route_table_ids" {
  value = [aws_route_table.public.id]
}

output "private_route_table_ids" {
  value = aws_route_table.private[*].id
}

output "nat_gateway_ids" {
  value = aws_nat_gateway.main[*].id
}

output "interface_endpoint_ids" {
  value = {
    for service, endpoint in aws_vpc_endpoint.interface :
    service => endpoint.id
  }
}

output "s3_endpoint_id" {
  value = aws_vpc_endpoint.s3.id
}

