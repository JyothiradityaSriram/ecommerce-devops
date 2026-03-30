resource "aws_s3_bucket" "frontend" {
  bucket = "my-ecommerce-frontend-12345"
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }
}
