
data "aws_iam_policy_document" "cross_account" {
  statement {
    sid    = "AllowEKSWorkloadAccess"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [var.workload_role_arn]
    }

    actions = var.allowed_actions

    resources = [
      var.dynamodb_table_arn,
      "${var.dynamodb_table_arn}/index/*"
    ]
  }
}

resource "aws_dynamodb_resource_policy" "cross_account" {
  resource_arn = var.dynamodb_table_arn
  policy       = data.aws_iam_policy_document.cross_account.json
}

