
variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "ap-southeast-2"
}

variable "project_name" {
  description = "Project name used for AWS resources"
  type        = string
  default     = "serverless-order-api"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
