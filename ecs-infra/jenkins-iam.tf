resource "aws_iam_user" "jenkins" {
  name = "jenkins-user"
}

resource "aws_iam_policy" "jenkins_policy" {
  name = "jenkins-ecr-ecs-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecs:UpdateService",
          "ecs:DescribeServices"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "attach" {
  user       = aws_iam_user.jenkins.name
  policy_arn = aws_iam_policy.jenkins_policy.arn
}
resource "aws_iam_role_policy_attachment" "jenkins_ecr_power_user" {
  user       = aws_iam_user.jenkins.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}
