#*************************************
#         TF auth Requirements
#*************************************
variable "tenancy_ocid" {
  type        = string
  description = "OCI tenant OCID, more details can be found at https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#five"
}
variable "region" {
  type        = string
  description = "OCI Region as documented at https://docs.cloud.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm"
}

variable "dynamic_group_name" {
  type        = string
  description = "The name of the dynamic group for giving access to service connector"
  default     = "chrono-metrics-dynamic-group"
}

variable "chrono_metrics_policy" {
  type        = string
  description = "The name of the policy for metrics"
  default     = "chrono-metrics-policy"
}

