variable "env" {
  description = "staging or prod environment"
  type        = string
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
}

variable "FIREBASE_ADMINSDK_CERTIFICATE" {
  description = "value"
  type        = string
  sensitive   = true
}

variable "REDDIT_API_KEY" {
  description = "value"
  type        = string
  sensitive   = true
}

variable "REDDIT_BASE_URL" {
  description = "value"
  type        = string
}

variable "REDDIT_CLIENT_ID" {
  description = "value"
  type        = string
}

variable "REDDIT_DATA_SOURCE" {
  description = "value"
  type        = string
}

variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}
