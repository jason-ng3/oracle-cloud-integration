resource "oci_functions_application" "metrics_function_app" {
  depends_on     = [data.oci_core_subnet.input_subnet]
  compartment_id = var.compartment_ocid
  config = {
    "CHRONO_COMPRESS" = "true"
    "OTEL_ENDPOINT"   = var.otel_collector_endpoint
    "CHRONO_MAX_POOL" = "20"
    "OCI_REGION"      = var.region
  }
  defined_tags  = {}
  display_name  = "${var.resource_name_prefix}-function-app"
  freeform_tags = local.freeform_tags
  network_security_group_ids = [
  ]
  shape = var.function_app_shape
  subnet_ids = [
    data.oci_core_subnet.input_subnet.id,
  ]
}

resource "oci_functions_function" "metrics_function" {
  depends_on = [null_resource.FnImagePushToOCIR, oci_functions_application.metrics_function_app]
  #Required
  application_id = oci_functions_application.metrics_function_app.id
  display_name   = "${oci_functions_application.metrics_function_app.display_name}-metrics-function"
  memory_in_mbs  = "256"

  #Optional
  defined_tags  = {}
  freeform_tags = local.freeform_tags
  image         = local.user_image_provided ? local.custom_image_path : local.docker_image_path
  image_digest  = local.user_image_provided ? null : data.oci_artifacts_container_image.function_image.digest
}
