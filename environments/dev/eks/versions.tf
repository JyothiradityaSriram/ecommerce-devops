
terraform {
  required_version = ">= 1.12.0"

  backend "s3" {
    bucket       = "ecommerce-devops-terraform-state-886682668143"
    key          = "environments/dev/eks/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "newaccount"
}

