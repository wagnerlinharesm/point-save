terraform {
  backend "s3" {
    bucket = "point-terraform-state"
    key    = "point-save.tfstate"
    region = "us-east-2"
    encrypt = true
  }
}