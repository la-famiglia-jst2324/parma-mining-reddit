variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}

/* ------------------------ Analytics and Sourcing Auth Flow ------------------------ */

variable "PARMA_SHARED_SECRET_KEY" {
  description = "Shared secret key for the analytics and sourcing auth flow"
  type        = string
  sensitive   = true
}

/* ------------------------------------ Reddit ------------------------------------ */


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
