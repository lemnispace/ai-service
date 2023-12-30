terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "lemnispace-terraform-state"
    key            = "ai-service/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region
}

data "terraform_remote_state" "lemnispace_services" {
  backend = "s3"
  config = {
    bucket         = "lemnispace-terraform-state"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }
}

module "ai_service_routes" {
  source            = "./modules/routes"
  lambda_endpoint   = var.root_path
  lambda_invoke_arn = module.ai_service_lambda.invoke_arn
  api_id            = data.terraform_remote_state.lemnispace_services.outputs.api_id
}

module "ai_service_lambda" {
  source                  = "./modules/lambda"
  allow_origins           = var.allow_origins
  root_path               = var.root_path
  stability_api_host      = var.stability_api_host
  stability_api_host_gen  = var.stability_api_host_gen
  s3_bucket_id            = data.terraform_remote_state.lemnispace_services.outputs.services_s3_bucket_id
  execute_lambda_role_arn = data.terraform_remote_state.lemnispace_services.outputs.execute_lambda_role_arn
}

resource "aws_lambda_permission" "ai_service_apigw_invoke_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.ai_service_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${data.terraform_remote_state.lemnispace_services.outputs.api_execution_arn}/*/*"
}
