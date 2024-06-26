terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/prod/mining/reddit"
    credentials = "../.secrets/la-famiglia-parma-ai.json"
  }
}

locals {
  project = "la-famiglia-parma-ai"
  region  = "europe-west1"
}

provider "google" {
  credentials = file("../.secrets/la-famiglia-parma-ai.json")
  project     = local.project
  region      = local.region
}

module "main" {
  source           = "../module"
  env              = "prod"
  project          = local.project
  region           = local.region
  REDDIT_API_KEY = var.REDDIT_API_KEY
  REDDIT_BASE_URL = var.REDDIT_BASE_URL
  REDDIT_CLIENT_ID = var.REDDIT_CLIENT_ID
  ANALYTICS_BASE_URL = var.ANALYTICS_BASE_URL

  PARMA_SHARED_SECRET_KEY = var.PARMA_SHARED_SECRET_KEY
}
