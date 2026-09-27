terraform {
  required_version = ">= 1.12.0"

  backend "s3" {
    bucket       = "ecommerce-devops-terraform-state-886682668143"
    key          = "ecs-infra/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}

provider "aws" {
  region = var.region
}
