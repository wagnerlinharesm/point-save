provider "aws" {
  region = var.region
}

resource "aws_iam_role" "point_save_iam_role" {
  name               = "point_save_iam_role"
  assume_role_policy = file("iam/policy/assume_role_policy.json")
}

data "aws_secretsmanager_secret" "point_db_secretsmanager_secret" {
  name = var.point_db_secretsmanager_secret
}

data "aws_secretsmanager_secret_version" "point_db_secretsmanager_secret_version" {
  secret_id = data.aws_secretsmanager_secret.point_db_secretsmanager_secret.id
}

locals {
  point_db_secrets = jsondecode(data.aws_secretsmanager_secret_version.point_db_secretsmanager_secret_version.secret_string)
}

resource "aws_lambda_function" "point_save_lambda_function" {
  function_name = "point_save"
  handler       = "app/lambda_function.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.point_save_iam_role.arn

  filename = "lambda_function.zip"

  source_code_hash = filebase64sha256("lambda_function.zip")

  depends_on = [
    aws_iam_role.point_save_iam_role
  ]

  environment {
    variables = {
      DB_HOST     = "point-db.cqivfynnpqib.us-east-2.rds.amazonaws.com:5432",
      DB_NAME     = "point_db",
      DB_USER     = local.point_db_secrets["username"],
      DB_PASSWORD = local.point_db_secrets["password"],
    }
  }
}