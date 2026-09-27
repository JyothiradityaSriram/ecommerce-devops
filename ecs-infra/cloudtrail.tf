
resource "aws_s3_bucket" "cloudtrail_logs" {
  bucket = "ecommerce-devops-cloudtrail-886682668143"

  tags = {
    Name        = "ecommerce-cloudtrail-logs"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_versioning" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudwatch_log_group" "cloudtrail" {
  name              = "/aws/cloudtrail/security"
  retention_in_days = 30

  tags = {
    Name = "cloudtrail-security-logs"
  }
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "cloudtrail_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "cloudtrail_cloudwatch" {
  name               = "CloudTrail_CloudWatchLogs_Role"
  assume_role_policy = data.aws_iam_policy_document.cloudtrail_assume_role.json
}

data "aws_iam_policy_document" "cloudtrail_cloudwatch" {
  statement {
    sid    = "CloudTrailCreateLogStream"
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "${aws_cloudwatch_log_group.cloudtrail.arn}:*"
    ]
  }
}

resource "aws_iam_role_policy" "cloudtrail_cloudwatch" {
  name   = "CloudTrailCloudWatchLogsPolicy"
  role   = aws_iam_role.cloudtrail_cloudwatch.id
  policy = data.aws_iam_policy_document.cloudtrail_cloudwatch.json
}

data "aws_iam_policy_document" "cloudtrail_s3" {
  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.cloudtrail_logs.arn]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values = [
        "arn:aws:cloudtrail:ap-south-1:${data.aws_caller_identity.current.account_id}:trail/ecommerce-security-trail"
      ]
    }
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions = ["s3:PutObject"]

    resources = [
      "${aws_s3_bucket.cloudtrail_logs.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"
    ]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values = [
        "arn:aws:cloudtrail:ap-south-1:${data.aws_caller_identity.current.account_id}:trail/ecommerce-security-trail"
      ]
    }
  }
}

resource "aws_s3_bucket_policy" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id
  policy = data.aws_iam_policy_document.cloudtrail_s3.json
}

resource "aws_cloudtrail" "security" {
  name                          = "ecommerce-security-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true

  cloud_watch_logs_group_arn = "${aws_cloudwatch_log_group.cloudtrail.arn}:*"
  cloud_watch_logs_role_arn  = aws_iam_role.cloudtrail_cloudwatch.arn

  depends_on = [
    aws_s3_bucket_policy.cloudtrail_logs,
    aws_iam_role_policy.cloudtrail_cloudwatch
  ]

  tags = {
    Name = "ecommerce-security-trail"
  }
}

resource "aws_sns_topic" "security_alerts" {
  name = "ecommerce-security-alerts"
}

variable "security_alert_email" {
  description = "Email address for security notifications"
  type        = string
}

resource "aws_sns_topic_subscription" "security_email" {
  topic_arn = aws_sns_topic.security_alerts.arn
  protocol  = "email"
  endpoint  = var.security_alert_email
}
resource "aws_cloudwatch_log_metric_filter" "cloudtrail_stop_logging" {
  name           = "CloudTrailStopLogging"
  log_group_name = aws_cloudwatch_log_group.cloudtrail.name

  pattern = "{ ($.eventName = StopLogging) }"

  metric_transformation {
    name      = "CloudTrailStopLoggingCount"
    namespace = "Security/CloudTrail"
    value     = "1"
  }
}
resource "aws_cloudwatch_metric_alarm" "cloudtrail_stop_logging" {
  alarm_name          = "cloudtrail-stop-logging"
  alarm_description   = "Alert when CloudTrail logging is stopped"

  namespace           = "Security/CloudTrail"
  metric_name         = "CloudTrailStopLoggingCount"

  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1

  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"

  alarm_actions = [
    aws_sns_topic.security_alerts.arn
  ]
}
