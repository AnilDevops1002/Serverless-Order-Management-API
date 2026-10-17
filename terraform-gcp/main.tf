resource "google_cloud_run_v2_service" "order_api" {
  name     = "order-api"
  location = "asia-south1"
  project  = "project-410d49a2-c36e-4d11-8aa"
  client   = "gcloud"

  deletion_protection = true

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
      client_version,
      client_version
    ]
  }
  ingress = "INGRESS_TRAFFIC_ALL"

  scaling {
    min_instance_count    = 0
    manual_instance_count = 0
  }

  template {
    service_account                  = "127867074951-compute@developer.gserviceaccount.com"
    timeout                          = "300s"
    max_instance_request_concurrency = 10

    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }

    containers {
      image = "asia-south1-docker.pkg.dev/project-410d49a2-c36e-4d11-8aa/order-api-repo/order-api:v1"

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }

      env {
        name  = "TELEMETRY_ENABLED"
        value = "false"
      }
    }
  }
}
