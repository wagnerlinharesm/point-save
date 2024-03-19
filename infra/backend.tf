terraform {
  backend "s3" {
    bucket         = "point-terraform-state"
    key            = "point-lambda-pre-sign-up.tfstate"
    region         = "us-east-2"
    encrypt        = true
  }
}