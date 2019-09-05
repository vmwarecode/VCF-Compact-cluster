Compact Cluster:

When a host is removed from a cluster in a domain, the vSAN members are reduced. Ensure that you have enough hosts remaining to facilitate the configured vSAN availability. Failure to do so might result in the datastore being marked as read-only or in data loss.

Prerequisites:

The following data is required

For each host to be removed

	->ID of the host


Usage: python compact_cluster.py <hostname> <username> <password> <cluster_id>

compact_cluster_spec.json is the input sample input specifications file.