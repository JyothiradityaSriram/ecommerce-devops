resource "aws_ecr_repository" "cart" {
  name                 = "cart-service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
