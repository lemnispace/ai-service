### S3 Bucket for Lambda Function ###
data "archive_file" "AIServiceFunction" {
  type        = "zip"
  source_dir  = "${path.root}/../.aws-sam/build/AIServiceFunction"
  output_path = "${path.root}/../.aws-sam/AIServiceFunction.zip"
}

resource "aws_s3_object" "ai_service" {
  bucket = var.s3_bucket_id
  key    = "AIServiceFunction.zip"

  source = data.archive_file.AIServiceFunction.output_path
  etag   = filemd5(data.archive_file.AIServiceFunction.output_path)
}

### CloudWatch Log Group with Retention ###
resource "aws_cloudwatch_log_group" "ai_service" {
  name              = "/aws/lambda/AIServiceFunction"
  retention_in_days = 30

  tags = {
    Name        = "AIServiceFunction"
    Environment = var.stage
    ManagedBy   = "Terraform"
  }
}

### Lambda Function ###
resource "aws_lambda_function" "AIServiceFunction" {
  filename         = data.archive_file.AIServiceFunction.output_path
  function_name    = "AIServiceFunction"
  role             = var.execute_lambda_role_arn
  handler          = "main.handler"
  runtime          = "python3.11"
  source_code_hash = data.archive_file.AIServiceFunction.output_base64sha256
  timeout          = 60
  memory_size      = 1024

  environment {
    variables = {
      ALLOWED_ORIGINS                 = var.allow_origins
      ROOT_PATH                       = var.root_path
      STABILITY_API_HOST              = var.stability_api_host
      STABILITY_API_HOST_GEN          = var.stability_api_host_gen
      AWS_PARAMETER_STORE_REGION_NAME = var.aws_parameter_store_region
      STABILITY_API_KEY_NAME          = var.stability_api_key_name
    }
  }

  # Ensure log group is created before Lambda
  depends_on = [aws_cloudwatch_log_group.ai_service]

  tags = {
    Name        = "AIServiceFunction"
    Environment = var.stage
    ManagedBy   = "Terraform"
  }
}

### Lambda Alias ###
resource "aws_lambda_alias" "ai_service" {
  name             = var.stage
  description      = "Alias for ${var.stage} environment"
  function_name    = aws_lambda_function.AIServiceFunction.arn
  function_version = "$LATEST"
}

### CloudWatch Alarms ###
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "AIServiceFunction-Errors-${var.stage}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Alert when Lambda function has more than 5 errors in 5 minutes"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.AIServiceFunction.function_name
  }

  tags = {
    Name        = "AIServiceFunction-Errors"
    Environment = var.stage
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "AIServiceFunction-Throttles-${var.stage}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "Alert when Lambda function is throttled more than 10 times in 5 minutes"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.AIServiceFunction.function_name
  }

  tags = {
    Name        = "AIServiceFunction-Throttles"
    Environment = var.stage
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "AIServiceFunction-Duration-${var.stage}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 50000 # 50 seconds
  alarm_description   = "Alert when Lambda duration exceeds 50 seconds average"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.AIServiceFunction.function_name
  }

  tags = {
    Name        = "AIServiceFunction-Duration"
    Environment = var.stage
    ManagedBy   = "Terraform"
  }
}

