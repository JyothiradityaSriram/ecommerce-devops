
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "jenkins" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "ecr" {
  statement {
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
      "ecr:BatchGetImage"
    ]

    resources = [
      "arn:aws:ecr:${var.region}:${var.account_id}:repository/${var.ecr_repository_name}"
    ]
  }
}

resource "aws_iam_policy" "ecr" {
  name   = "${var.role_name}-ECRPolicy"
  policy = data.aws_iam_policy_document.ecr.json
}

resource "aws_iam_role_policy_attachment" "ecr" {
  role       = aws_iam_role.jenkins.name
  policy_arn = aws_iam_policy.ecr.arn
}

data "aws_iam_policy_document" "eks" {
  statement {
    effect  = "Allow"
    actions = ["eks:DescribeCluster"]
    resources = [
      "arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}"
    ]
  }
}

resource "aws_iam_policy" "eks" {
  name   = "${var.role_name}-EKSDescribeClusterPolicy"
  policy = data.aws_iam_policy_document.eks.json
}

resource "aws_iam_role_policy_attachment" "eks" {
  role       = aws_iam_role.jenkins.name
  policy_arn = aws_iam_policy.eks.arn
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.jenkins.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "jenkins" {
  name = "${var.role_name}-InstanceProfile"
  role = aws_iam_role.jenkins.name
}

