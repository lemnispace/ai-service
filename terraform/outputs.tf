output "AIServiceFunction_name" {
  description = "The name of the lambda function"
  value       = module.ai_service_lambda.function_name
}

output "AIServiceFunction_arn" {
  description = "The ARN of the lambda function"
  value       = module.ai_service_lambda.arn
}

output "AIServiceFunction_invoke_arn" {
  description = "The invoke ARN of the lambda function"
  value       = module.ai_service_lambda.invoke_arn
}

output "ai_service_route_id" {
  description = "The ID of the ai_service service route"
  value       = module.ai_service_routes.route_id
}

output "ai_service_route_uri" {
  description = "The URI of the ai_service service route"
  value       = module.ai_service_routes.route_uri
}

output "ai_service_route_hash" {
  description = "The hash of the ai_service service route. Used for deployments to trigger when the route changes"
  value       = module.ai_service_routes.route_hash
}
