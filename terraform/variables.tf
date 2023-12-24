variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-1"
}

variable "stage" {
  description = "Stage for the API Gateway where the lambda function will be deployed to"
  type        = string
  default     = "Dev"
}

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

variable "stability_api_key" {
  description = "API key for the Stability API"
  type        = string
  default     = "replace-me"
  sensitive   = true
}

variable "stability_api_host" {
  description = "Host for the Stability API"
  type        = string
  default     = "https://api.stability.ai"
}

variable "stability_api_host_gen" {
  description = "Host for the Stability API"
  type        = string
  default     = "https://api.stability.ai/v1/generation"
}
