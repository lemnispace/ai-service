output "invoke_arn" {
  description = "ARN of the lambda function"
  value       = aws_lambda_function.AIServiceFunction.invoke_arn
}

output "function_name" {
  description = "Name of the lambda function"
  value       = aws_lambda_function.AIServiceFunction.function_name
}
