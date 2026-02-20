# -----------------------------
# ECR Repositories
# -----------------------------
resource "aws_ecrpublic_repository" "train" {
  repository_name                 = "${var.project}-train"
}

resource "aws_ecrpublic_repository" "inference" {
  repository_name                 = "${var.project}-inference"
}

