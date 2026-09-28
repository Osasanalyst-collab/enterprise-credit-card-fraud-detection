terraform { required_version = ">= 1.7.0" }
variable "environment" { type = string; default = "development" }
# Add provider-specific modules for managed PostgreSQL, container registry,
# Kubernetes/container apps, object storage, secrets and monitoring.
output "environment" { value = var.environment }
