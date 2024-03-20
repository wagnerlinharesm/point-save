variable "region" {
  type    = string
  default = "us-east-2"
}

variable "point_db_secretsmanager_secret" {
  type    = string
  default = "mikes/db/db_credentials"
}

variable "point_db_host" {
    type    = string
    default = "point-db.cqivfynnpqib.us-east-2.rds.amazonaws.com"
}

variable "point_db_name" {
    type    = string
    default = "pointdb"
}