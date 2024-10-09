## OCI Integration
The OCI integration consists of two OCI resource manager (ORM) Terrform stacks:

1. A policy stack to create a dynamic group that contains the Connector Hub and the associated permissions policy to allow the dynamic group to read and invoke OCI functions.
2. A metric stack to deploy the Connector Hub, OCI function application, and networking infrastructure (if necessary) for the metrics pipeline from OCI Monitoring to the OTel Collector.