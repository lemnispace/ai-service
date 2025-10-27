variable "allow_origins" {
  description = "Comma-separated list of allowed origins for CORS"
  type        = string
  default     = "*"
}

variable "root_path" {
  description = "Root path for the API Gateway where the lambda function will be deployed to"
  type        = string
  default     = "gen/ai"
}

variable "stability_api_host" {
  description = "Host for the Stability API"
  type        = string
}

variable "stability_api_host_gen" {
  description = "Host for the Stability API"
  type        = string
}

variable "s3_bucket_id" {
  description = "ID of the S3 bucket where the lambda function will be deployed to"
  type        = string
}

variable "execute_lambda_role_arn" {
  description = "ARN of the role that will be used to execute the lambda function. This is used to give the API Gateway permission to invoke the lambda function"
  type        = string
}

variable "aws_parameter_store_region" {
  description = "AWS region where the parameter store is located"
  type        = string
}

variable "stability_api_key_name" {
  description = "Name of the parameter in the parameter store that contains the API key for the Stability API"
  type        = string
}

variable "stage" {
  description = "Stage for the API Gateway where the lambda function will be deployed to"
  type        = string
  default     = "Dev"
}
