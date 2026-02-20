# -----------------------------
# IAM role for SageMaker
# -----------------------------
data "aws_iam_policy_document" "sagemaker_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sagemaker_exec" {
  name               = "${var.project}-sagemaker-role"
  assume_role_policy = data.aws_iam_policy_document.sagemaker_assume.json
}

# Minimal permissions: S3 + ECR pull + CloudWatch logs
data "aws_iam_policy_document" "sagemaker_policy" {
  statement {
    actions = ["s3:ListBucket"]
    resources = [aws_s3_bucket.data.arn]
  }

  statement {
    actions = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.data.arn}/*"]
  }

  statement {
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchCheckLayerAvailability"
    ]
    resources = ["*"]
  }

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "sagemaker_inline" {
  role   = aws_iam_role.sagemaker_exec.id
  policy = data.aws_iam_policy_document.sagemaker_policy.json
}
