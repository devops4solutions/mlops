# -----------------------------
# ECR Repositories
# -----------------------------
resource "aws_ecr_repository" "train" {
  name                 = "${var.project}-train"
}

resource "aws_ecr_repository" "inference" {
  name                 = "${var.project}-inference"
}

