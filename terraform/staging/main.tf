terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/staging/mining/reddit"
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
  env              = "staging"
  project          = local.project
  region           = local.region
  FIREBASE_ADMINSDK_CERTIFICATE = var.FIREBASE_ADMINSDK_CERTIFICATE
  REDDIT_API_KEY = var.REDDIT_API_KEY
  REDDIT_BASE_URL = var.REDDIT_BASE_URL
  REDDIT_CLIENT_ID = var.REDDIT_CLIENT_ID
  REDDIT_DATA_SOURCE = var.REDDIT_DATA_SOURCE
  ANALYTICS_BASE_URL = var.ANALYTICS_BASE_URL
}
