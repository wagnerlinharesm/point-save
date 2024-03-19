provider "aws" {
  region = var.region
}

resource "aws_iam_role" "point_lambda_pre_sign_up_role" {
  name               = "point_lambda_pre_sign_up_role"
  assume_role_policy = file("policy/lambda_assume_role_policy.json")
}

resource "aws_lambda_function" "point_lambda_pre_sign_up" {
  function_name = "point_lambda_pre_sign_up"
  handler       = "app/lambda_function.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.point_lambda_pre_sign_up_role.arn

  filename = "lambda_function.zip"

  source_code_hash = filebase64sha256("lambda_function.zip")

  depends_on = [
    aws_iam_role.point_lambda_pre_sign_up_role
  ]
}