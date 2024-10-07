## Deploy to OCI (metrics)

The setup creates an OCI resource manager (ORM) stack which uses terraform to:

* Create OCI resources on OCI send metrics to Chronosphere using Connector Hub & OCI Functions
* Create policies in order to allow Connector Hub to read metrics from different tenancy compartments