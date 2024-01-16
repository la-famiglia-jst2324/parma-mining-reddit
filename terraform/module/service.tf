
/* ---------------------------------- Service Image --------------------------------- */

# Note: Generally it is NOT best practise to build images in Terraform. We are still
# doing it here for simplicity. In industry, you should think twice before doing this.
resource "null_resource" "docker_build" {

  provisioner "local-exec" {
    working_dir = path.module
    command     = "IMG=${var.region}-docker.pkg.dev/${var.project}/parma-registry/parma-mining-reddit:${var.env}-$(git rev-parse --short HEAD) && docker build -t $IMG ./../../ && docker push $IMG && echo $IMG > .image.name"
  }

  triggers = {
    always_run = timestamp()
  }
}

# get output from docker_build
data "local_file" "image_name" {
  filename   = "${path.module}/.image.name"
  depends_on = [null_resource.docker_build]
}


/* ------------------------------------ Cloud Run ----------------------------------- */

resource "google_cloud_run_service" "parma_mining_reddit_cloud_run" {
  name     = "parma-mining-reddit-${var.env}"
  location = var.region

  template {
    spec {
      containers {
        image = data.local_file.image_name.content
        ports {
          container_port = 8080
        }
        env {
          name  = "REDDIT_API_KEY"
          value = var.REDDIT_API_KEY
        }
        env {
          name  = "REDDIT_BASE_URL"
          value = var.REDDIT_BASE_URL
        }
        env {
          name  = "REDDIT_CLIENT_ID"
          value = var.REDDIT_CLIENT_ID
        }
        env {
          name  = "REDDIT_DATA_SOURCE"
          value = var.REDDIT_DATA_SOURCE
        }
        env {
          name  = "ANALYTICS_BASE_URL"
          value = var.ANALYTICS_BASE_URL
        }
        env {
          name  = "PARMA_SHARED_SECRET_KEY"
          value = var.PARMA_SHARED_SECRET_KEY
        }
        env {
          name  = "DEPLOYMENT_ENV"
          value = var.env
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

/* --------------------------------------- IAM -------------------------------------- */

// Define a policy that allows any user to invoke the Cloud Run service.
data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

// Apply the policy to the Cloud Run service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.parma_mining_reddit_cloud_run.location
  project  = google_cloud_run_service.parma_mining_reddit_cloud_run.project
  service  = google_cloud_run_service.parma_mining_reddit_cloud_run.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
