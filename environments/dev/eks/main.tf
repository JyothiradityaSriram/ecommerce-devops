
module "network" {
  source = "../../../modules/network"

  name               = "ecommerce-${var.environment}"
  aws_region         = var.aws_region
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones

  enable_nat_gateway         = var.enable_nat_gateway
  nat_gateway_count          = 1
  enable_interface_endpoints = var.enable_interface_endpoints
}


module "eks" {
  source = "../../../modules/eks"

  cluster_name       = "ecommerce-${var.environment}"
  eks_version        = "1.34"
  private_subnet_ids = module.network.private_subnet_ids

  node_instance_types = ["t3.small"]
  node_desired_size   = 0
  node_min_size       = 0
  node_max_size       = 2
}

module "cart_workload_role" {
  source = "../../../modules/iam-workload-role"

  role_name          = "ecommerce-dev-cart-workload-role"
  cluster_name       = module.eks.cluster_name
  aws_region         = var.aws_region
  dynamodb_table_arn = "arn:aws:dynamodb:ap-south-1:542175649814:table/cart"
}

resource "aws_eks_pod_identity_association" "cart_service" {
  cluster_name    = module.eks.cluster_name
  namespace       = "default"
  service_account = "cart-service-sa"
  role_arn        = module.cart_workload_role.role_arn

  depends_on = [module.eks]
}
