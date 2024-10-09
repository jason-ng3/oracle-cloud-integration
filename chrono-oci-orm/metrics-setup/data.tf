# Source from https://registry.terraform.io/providers/oracle/oci/latest/docs/data-sources/identity_region_subscriptions

data "oci_identity_region_subscriptions" "subscriptions" {
  # Required
  provider   = oci.home
  tenancy_id = var.tenancy_ocid
}

data "oci_objectstorage_namespace" "namespace" {
  provider       = oci.home
  compartment_id = var.tenancy_ocid
}

data "oci_identity_tenancy" "tenancy_metadata" {
  tenancy_id = var.tenancy_ocid
}

data "oci_core_subnet" "input_subnet" {
  depends_on = [module.vcn]
  #Required
  subnet_id = var.create_vcn ? module.vcn[0].subnet_id[local.subnet] : var.function_subnet_id
}

data "oci_artifacts_container_image" "function_image" {
  compartment_id = var.compartment_id
  repository     = "${local.oci_region_key}.ocir.io/${local.ocir_namespace}/${local.ocir_repo_name}"
  version        = "latest"
}