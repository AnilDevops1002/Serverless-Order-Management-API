terraform {
  backend "gcs" {
    bucket = "project-410d49a2-c36e-4d11-8aa-tfstate"
    prefix = "order-api/terraform/state"
  }
}
