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
