### S3 Bucket for Lambda Function ###
data "archive_file" "AIServiceFunction" {
  type        = "zip"
  source_dir  = "${path.module}/../.aws-sam/build/AIServiceFunction"
  output_path = "${path.module}/../.aws-sam/AIServiceFunction.zip"
}

resource "aws_s3_object" "ai_service" {
  bucket = var.s3_bucket_id
  key    = "AIServiceFunction.zip"

  source = data.archive_file.AIServiceFunction.output_path
  etag   = filemd5(data.archive_file.AIServiceFunction.output_path)
}

### Lambda Function ###
resource "aws_lambda_function" "AIServiceFunction" {
  filename         = data.archive_file.AIServiceFunction.output_path
  function_name    = "AIServiceFunction"
  role             = var.execute_lambda_role_arn
  handler          = "main.handler"
  runtime          = "python3.11"
  source_code_hash = data.archive_file.AIServiceFunction.output_base64sha256
  timeout          = 30
  memory_size      = 512
  environment {
    variables = {
      ALLOWED_ORIGINS        = var.allow_origins
      ROOT_PATH              = var.root_path
      STABILITY_API_HOST     = var.stability_api_host
      STABILITY_API_HOST_GEN = var.stability_api_host_gen
    }
  }
}

