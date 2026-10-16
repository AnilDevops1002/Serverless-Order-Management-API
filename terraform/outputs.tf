
output "api_gateway_url" {
  description = "Base URL of the Order Management HTTP API"
  value       = aws_apigatewayv2_stage.default.invoke_url
}

output "lambda_function_name" {
  description = "Name of the deployed Lambda function"
  value       = aws_lambda_function.order_api.function_name
}
