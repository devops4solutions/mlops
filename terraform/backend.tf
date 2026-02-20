terraform {
  backend "s3" {
    bucket         = "devops4solutions-terraform"
    key            = "mlops/terraform.tfstate"
    region         = "us-east-1"
  }
}
