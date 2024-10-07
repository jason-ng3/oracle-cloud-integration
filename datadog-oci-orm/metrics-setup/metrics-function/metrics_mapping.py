import re
import json

"""
Table of OCI metrics collected: 
https://docs.datadoghq.com/integrations/oracle_cloud_infrastructure
"""

text = """
oci.autonomous.database.apply.lag
(gauge)	This metric displays (in seconds) how far the standby database is behind the primary database as of the time sampled.
Shown as second
oci.autonomous.database.block.changes
(gauge)	The average number of blocks changed per second.
Shown as update
oci.autonomous.database.cpu.time
(gauge)	Average rate of accumulation of CPU time by foreground sessions in the database over the time interval. Statistic: Mean. Interval: 1 minute
Shown as second
oci.autonomous.database.cpu.utilization
(gauge)	The CPU usage expressed as a percentage, aggregated across all consumer groups. The utilization percentage is reported with respect to the number of CPUs the database is allowed to use. Statistic: Mean. Interval: 1 minute
Shown as percent
oci.autonomous.database.current.logons
(count)	The number of successful logons during the selected interval. Statistic: Count. Interval: 1 minute
Shown as operation
oci.autonomous.database.dbtime
(gauge)	The amount of time database user sessions spend executing database code (CPU Time + WaitTime). DB Time is used to infer database call latency, because DB Time increases in direct proportion to both database call latency (response time) and call volume. It is calculated as the average rate of accumulation of database time by foreground sessions in the database over the time interval.
Shown as second
oci.autonomous.database.ecpus.allocated
(gauge)	The actual number of ECPUs allocated by the service during the selected interval of time.
Shown as cpu
oci.autonomous.database.execute.count
(count)	The number of user and recursive calls that executed SQL statements during the selected interval. Statistic: Sum. Interval: 1 minute
Shown as execution
oci.autonomous.database.iops
(gauge)	The average number of I/O operations per second.
Shown as operation
oci.autonomous.database.iothroughput
(gauge)	The average throughput in MB per second.
Shown as megabyte
oci.autonomous.database.logical.blocks.read
(gauge)	The average number of logical block reads ("db block gets" plus "consistent gets") per second. Includes buffered and direct I/O. Statistic: Sum. Interval: 1 minute
Shown as read
oci.autonomous.database.ocpus.allocated
(gauge)	The actual number of OCPUs allocated by the service during the selected interval of time.
Shown as cpu
oci.autonomous.database.parse.count
(count)	The number of hard and soft parses during the selected interval. Statistic: Sum. Interval: 1 minute
Shown as event
oci.autonomous.database.parses.by.type
(count)	The number of hard or soft parses per second.
Shown as event
oci.autonomous.database.queued.statements
(count)	The number of queued SQL statements, aggregated across all consumer groups, during the selected interval. Statistic: Sum. Interval: 1 minute
Shown as execution
oci.autonomous.database.redo.size
(gauge)	The average amount of redo generated in MB per second.
Shown as megabyte
oci.autonomous.database.running.statements
(count)	The number of running SQL statements, aggregated across all consumer groups, during the selected interval. Statistic: Mean. Interval: 1 minute
Shown as execution
oci.autonomous.database.sessions
(count)	The number of sessions in the database. Statistic: Sum. Interval: 1 minute
Shown as session
oci.autonomous.database.storage.allocated
(gauge)	Maximum amount of space allocated to the database during the interval. Statistic: Max. Interval: 1 hour
Shown as gigabyte
oci.autonomous.database.storage.allocated.by.tablespace
(gauge)	Maximum amount of space allocated for each tablespace during the interval.
Shown as gigabyte
oci.autonomous.database.storage.used
(gauge)	Maximum amount of space used during the interval. Statistic: Max. Interval: 1 hour
Shown as gigabyte
oci.autonomous.database.storage.used.by.tablespace
(gauge)	Maximum amount of space used by each tablespace during the interval.
Shown as gigabyte
oci.autonomous.database.storage.utilization
(gauge)	The percentage of provisioned storage capacity currently in use. Represents the total allocated space for all tablespaces. Statistic: Mean. Interval: 1 hour
Shown as percent
oci.autonomous.database.storage.utilization.by.tablespace
(gauge)	The percentage of space utilized by each tablespace.
Shown as percent
oci.autonomous.database.transaction.count
(count)	The combined number of user commits and user rollbacks during the selected interval. Statistic: Sum. Interval: 1 minute
Shown as event
oci.autonomous.database.transactions.by.status
(count)	The number of committed or rolled back transactions per second.
Shown as transaction
oci.autonomous.database.transport.lag
(gauge)	The approximate number of seconds of redo not yet available on the standby database as of the time sampled.
Shown as second
oci.autonomous.database.user.calls
(count)	The combined number of logons, parses, and execute calls during the selected interval. Statistic: Sum. Interval: 1 minute
Shown as event
oci.autonomous.database.wait.time
(gauge)	Average rate of accumulation of non-idle wait time by foreground sessions in the database over the time interval. Statistic: Mean. Interval: 1 minute
Shown as second
oci.database.block.changes
(gauge)	The Average number of blocks changed per second.
Shown as update
oci.database.cpu.utilization
(gauge)	The CPU utilization expressed as a percentage, aggregated across all consumer groups. The utilization percentage is reported with respect to the number of CPUs the database is allowed to use, which is two times the number of OCPUs.
Shown as percent
oci.database.current.logons
(count)	The number of successful logons during the selected interval.
oci.database.execute.count
(count)	The number of user and recursive calls that executed SQL statements during the selected interval.
oci.database.parse.count
(count)	The number of hard and soft parses during the selected interval.
oci.database.storage.allocated
(gauge)	Total amount of storage space allocated to the database at the collection time.
Shown as gigabyte
oci.database.storage.allocated.by.tablespace
(gauge)	Total amount of storage space allocated to the tablespace at the collection time. In case of container database, this metric provides root container tablespaces.
Shown as gigabyte
oci.database.storage.used
(gauge)	Total amount of storage space used by the database at the collection time.
Shown as gigabyte
oci.database.storage.used.by.tablespace
(gauge)	Total amount of storage space used by tablespace at the collection time. In case of container database, this metric provides root container tablespaces.
Shown as gigabyte
oci.database.storage.utilization
(gauge)	The percentage of provisioned storage capacity currently in use. Represents the total allocated space for all tablespaces.
Shown as percent
oci.database.storage.utilization.by.tablespace
(gauge)	This indicates the percentage of storage space utilized by the tablespace at the collection time. In case of container database, this metric provides root container tablespaces.
Shown as percent
oci.database.transaction.count
(count)	The combined number of user commits and user rollbacks during the selected interval.
Shown as transaction
oci.database.user.calls
(count)	The combined number of logons, parses, and execute calls during the selected interval.
oci.database.cluster.asmdiskgroup.utilization
(gauge)	Percentage of usable space used in a Disk Group. Usable space is the space available for growth. DATA disk group stores our Oracle database files. RECO disk group contains database files for recovery such as archives and flashback logs.
Shown as percent
oci.database.cluster.cpu.utilization
(gauge)	Percent CPU utilization.
Shown as percent
oci.database.cluster.filesystem.utilization
(gauge)	Percent utilization of provisioned filesystem.
Shown as percent
oci.database.cluster.load.average
(gauge)	System load average over 5 minutes.
Shown as process
oci.database.cluster.memory.utilization
(gauge)	Percentage of memory available for starting new applications, without swapping. The available memory can be obtained via the following command: cat/proc/meminfo.
Shown as percent
oci.database.cluster.node.status
(gauge)	Indicates whether the host is reachable in RAC environments.
oci.database.cluster.ocpus.allocated
(gauge)	The number of OCPUs allocated.
Shown as cpu
oci.database.cluster.swap.utilization
(gauge)	Percent utilization of total swap space.
Shown as percent
oci.blockstore.volume.guaranteed.iops
(gauge)	Rate of change for guaranteed IOPS per SLA. Expressed as the average of guaranteed IOPS during a given time interval.
Shown as operation
oci.blockstore.volume.guaranteed.throughput
(gauge)	Rate of change for guaranteed throughput per SLA. Expressed as megabytes per interval.
Shown as megabyte
oci.blockstore.volume.guaranteed.vpus.per.gb
(gauge)	Rate of change for currently active VPUs/GB. Expressed as the average of active VPUs/GB during a given time interval.
Shown as operation
oci.blockstore.volume.read.ops
(count)	Activity level from I/O reads. Expressed as reads per interval.
Shown as operation
oci.blockstore.volume.read.throughput
(gauge)	Read throughput. Expressed as bytes read per interval.
Shown as byte
oci.blockstore.volume.replication.seconds.since.last.sync
(gauge)	Time elapsed since the last synced cross region replica. Expressed in seconds.
Shown as second
oci.blockstore.volume.replication.seconds.since.last.upload
(gauge)	Time elapsed since the last cross region replica was uploaded. Expressed in seconds.
Shown as second
oci.blockstore.volume.throttled.ios
(count)	Total sum of all the I/O operations that were throttled during a given time interval.
Shown as operation
oci.blockstore.volume.write.ops
(count)	Activity level from I/O writes. Expressed as writes per interval.
Shown as operation
oci.blockstore.volume.write.throughput
(gauge)	Write throughput. Expressed as bytes written per interval.
Shown as byte
oci.gpu.infrastructure.health.gpu.ecc.double.bit.errors
(count)	The number of GPU double bit ECC errors reported.
Shown as error
oci.gpu.infrastructure.health.gpu.ecc.single.bit.errors
(count)	The number of GPU single bit ECC errors reported.
Shown as error
oci.gpu.infrastructure.health.gpu.memory.utilization
(gauge)	The percentage of the GPU memory resource in use.
Shown as percent
oci.gpu.infrastructure.health.gpu.power.draw
(gauge)	The amount of GPU power used.
oci.gpu.infrastructure.health.gpu.temperature
(gauge)	The GPU temperature reported.
oci.gpu.infrastructure.health.gpu.utilization
(gauge)	Activity level from GPU. Expressed as a percentage of total time. For instance pools, the value is averaged across all instances in the pool.
Shown as percent
oci.computeagent.cpu.utilization
(gauge)	Activity level from CPU. Expressed as a percentage of total time. For instance pools, the value is averaged across all instances in the pool.
Shown as percent
oci.computeagent.disk.bytes.read
(count)	Read throughput. Expressed as bytes read per interval.
Shown as byte
oci.computeagent.disk.bytes.written
(count)	Write throughput. Expressed as bytes written per interval.
Shown as byte
oci.computeagent.disk.iops.read
(count)	Activity level from I/O reads. Expressed as reads per interval.
Shown as operation
oci.computeagent.disk.iops.written
(count)	Activity level from I/O writes. Expressed as writes per interval.
Shown as operation
oci.computeagent.load.average
(gauge)	Average system load calculated over a 1-minute period.
Shown as process
oci.computeagent.memory.allocation.stalls
(count)	Number of times page reclaim was called directly.
oci.computeagent.memory.utilization
(gauge)	Space currently in use. Measured by pages. Expressed as a percentage of used pages. For instance pools, the value is averaged across all instances in the pool.
Shown as percent
oci.computeagent.networks.bytes.in
(count)	Network receipt throughput. Expressed as bytes received.
Shown as byte
oci.computeagent.networks.bytes.out
(count)	Network transmission throughput. Expressed as bytes transmitted.
Shown as byte
oci.rdma.infrastructure.health.rdma.rx.bytes
(count)	The bytes received on the RDMA interface.
Shown as byte
oci.rdma.infrastructure.health.rdma.rx.packets
(count)	The number of RDMA interface packets received.
Shown as packet
oci.rdma.infrastructure.health.rdma.tx.bytes
(count)	The bytes transmitted on the RDMA interface.
Shown as byte
oci.rdma.infrastructure.health.rdma.tx.packets
(count)	The number of RDMA interface packets transmitted.
Shown as packet
oci.compute.infrastructure.health.health.status
(count)	The number of health issues for an instance. Any non-zero value indicates a health defect. This metric is available only for bare metal instances.
Shown as error
oci.compute.infrastructure.health.instance.status
(gauge)	The status of a running instance. A value of 0 indicates that the instance is available (up). A value of 1 indicates that the instance is not available (down) due to an infrastructure issue. If the instance is stopped, then the metric does not have a value. This metric is available only for VM instances.
Shown as instance
oci.compute.infrastructure.health.maintenance.status
(gauge)	The maintenance status of an instance. A value of 0 indicates that the instance is not scheduled for an infrastructure maintenance event. A value of 1 indicates that the instance is scheduled for an infrastructure maintenance event. This metric is available for both VM and bare metal instances.
Shown as instance
oci.oracle.oci.database.allocated.storage.utilization.by.tablespace
(gauge)	The percentage of space used by a tablespace, out of allocated space.
Shown as percent
oci.oracle.oci.database.apply.lag
(gauge)	The number of seconds the standby database is behind the primary database. Statistic: Mean Interval: 5 minutes Resource group: oracle.dataguard Not applicable for PDBs.
Shown as second
oci.oracle.oci.database.apply.lag.data.refresh.elapsed.time
(gauge)	The elapsed time since the ApplyLag metric sample was last collected. Statistic: Mean Interval: 5 minutes Resource group: oracle.dataguard Not applicable for PDBs.
Shown as second
oci.oracle.oci.database.avg.gc.cr.block.receive.time
(gauge)	The average global cache consistent-read (CR) block receive time.
Shown as millisecond
oci.oracle.oci.database.backup.duration
(gauge)	The duration of the last database backup. Statistic: Mean Interval: 30 minutes Only applicable for SI and RAC CDBs.
Shown as second
oci.oracle.oci.database.backup.size
(gauge)	The size of the last database backup. Statistic: Mean Interval: 30 minutes Only applicable for SI and RAC CDBs.
Shown as gigabyte
oci.oracle.oci.database.block.changes
(gauge)	The average number of blocks changed per second.
Shown as update
oci.oracle.oci.database.blocking.sessions
(gauge)	The current blocking sessions.
oci.oracle.oci.database.cputime
(gauge)	The average rate of accumulation of CPU time by foreground sessions in the database instance over the time interval. The CPU time component of Average Active Sessions.
Shown as fraction
oci.oracle.oci.database.cpu.utilization
(gauge)	The CPU utilization expressed as a percentage, aggregated across all consumer groups. The utilization percentage is reported with respect to the number of CPUs the database is allowed to use, which is two times the number of OCPUs.
Shown as percent
oci.oracle.oci.database.current.logons
(count)	The number of successful logons during the selected interval.
oci.oracle.oci.database.dbtime
(gauge)	The average rate of accumulation of database time (CPU + Wait) by foreground sessions in the database instance over the time interval. Also known as Average Active Sessions.
Shown as fraction
oci.oracle.oci.database.estimated.failover.time
(gauge)	The number of seconds required to fail over to the standby database. Statistic: Mean. Interval: 5 minutes. Resource group: oracle.dataguard. Not applicable for PDBs.
Shown as second
oci.oracle.oci.database.execute.count
(count)	The number of user and recursive calls that executed SQL statements during the selected interval.
Shown as execution
oci.oracle.oci.database.fraspace.limit
(gauge)	The flash recovery area space limit.
Shown as gigabyte
oci.oracle.oci.database.frautilization
(gauge)	The flash recovery area utilization.
Shown as percent
oci.oracle.oci.database.gc.cr.blocks.received
(gauge)	The global cache CR blocks received per second.
Shown as block
oci.oracle.oci.database.gc.current.blocks.received
(gauge)	The global cache current blocks received per second.
Shown as block
oci.oracle.oci.database.iops
(gauge)	The average number of IO operations per second.
Shown as operation
oci.oracle.oci.database.io.throughput
(gauge)	The average throughput in MB per second.
Shown as megabyte
oci.oracle.oci.database.interconnect.traffic
(gauge)	The average internode data transfer rate.
Shown as megabyte
oci.oracle.oci.database.invalid.objects
(gauge)	The number of invalid database objects.
oci.oracle.oci.database.logical.blocks.read
(gauge)	The average number of blocks read from SGA/Memory (buffer cache) per second.
Shown as read
oci.oracle.oci.database.max.tablespace.size
(gauge)	The maximum possible tablespace size. For CDBs, this metric provides data for root container tablespaces.
Shown as gigabyte
oci.oracle.oci.database.memory.usage
(gauge)	The total size of the memory pool.
Shown as megabyte
oci.oracle.oci.database.monitoring.status
(gauge)	The monitoring status of the resource. If a metric collection fails, error information is captured in this metric.
oci.oracle.oci.database.non.reclaimable.fra
(gauge)	The non-reclaimable fast recovery area.
Shown as percent
oci.oracle.oci.database.ocpus.allocated
(count)	The actual number of OCPUs allocated by the service during the selected interval of time.
oci.oracle.oci.database.parse.count
(count)	The number of hard and soft parses during the selected interval.
oci.oracle.oci.database.parses.by.type
(gauge)	The number of hard or soft parses per second.
Shown as event
oci.oracle.oci.database.problematic.scheduled.dbmsjobs
(gauge)	The number of problematic scheduled database jobs.
Shown as job
oci.oracle.oci.database.process.limit.utilization
(gauge)	The process limit utilization.
Shown as percent
oci.oracle.oci.database.processes
(gauge)	The number of database processes.
Shown as process
oci.oracle.oci.database.reclaimable.fra
(gauge)	The reclaimable fast recovery area.
Shown as percent
oci.oracle.oci.database.reclaimable.fraspace
(gauge)	The flash recovery area reclaimable space.
Shown as gigabyte
oci.oracle.oci.database.recovery.window
(gauge)	The current recovery window of a database. Statistic: Mean. Interval: 15 minutes. Only applicable for SI and RAC CDBs version 19c and later.
Shown as second
oci.oracle.oci.database.redo.apply.rate
(gauge)	The redo apply rate on the standby database. Statistic: Mean. Interval: 5 minutes. Resource group: oracle.dataguard. Not applicable for PDBs.
Shown as megabyte
oci.oracle.oci.database.redo.generation.rate
(gauge)	The redo generation rate on the primary database. Statistic: Mean. Interval: 5 minutes. Resource group: oracle.dataguard. Not applicable for PDBs.
Shown as megabyte
oci.oracle.oci.database.redo.size
(gauge)	The average amount of redo generated.
Shown as megabyte
oci.oracle.oci.database.session.limit.utilization
(gauge)	The session limit utilization.
Shown as percent
oci.oracle.oci.database.sessions
(gauge)	The number of sessions in the database.
Shown as session
oci.oracle.oci.database.storage.allocated
(gauge)	The total amount of storage space allocated to the database at collection time.
Shown as gigabyte
oci.oracle.oci.database.storage.allocated.by.tablespace
(gauge)	The total amount of storage space allocated to the tablespace at collection time. In the case of CDBs, this metric provides root container tablespaces.
Shown as gigabyte
oci.oracle.oci.database.storage.used
(gauge)	The total storage used by the database at collection time, including the space used by tablespaces, flash recovery area, control files, and log files.
Shown as gigabyte
oci.oracle.oci.database.storage.used.by.tablespace
(gauge)	The total amount of storage space used by tablespace at collection time. In the case of CDBs, this metric provides root container tablespace.
Shown as gigabyte
oci.oracle.oci.database.storage.utilization
(gauge)	The percentage of provisioned storage capacity currently in use. Represents the total allocated space for all tablespaces.
Shown as percent
oci.oracle.oci.database.storage.utilization.by.tablespace
(gauge)	The percentage of storage space utilized by the tablespace at the collection time. In the case of CDBs, this metric provides root container tablespaces.
Shown as percent
oci.oracle.oci.database.transaction.count
(count)	The combined number of user commits and user rollbacks during the selected interval.
Shown as transaction
oci.oracle.oci.database.transactions.by.status
(gauge)	The number of committed or rolled back transactions per second.
Shown as transaction
oci.oracle.oci.database.transport.lag
(gauge)	The number of seconds of redo not yet available on the standby database. Statistic: Mean. Interval: 5 minutes. Resource group: oracle.dataguard. Not applicable for PDBs.
Shown as second
oci.oracle.oci.database.transport.lag.data.refresh.elapsed.time
(gauge)	The elapsed time since the TransportLagDataRefreshElapsedTime metric sample was last collected. Statistic: Mean. Interval: 5 minutes. Resource group: oracle.dataguard. Not applicable for PDBs.
Shown as second
oci.oracle.oci.database.unprotected.data.window
(gauge)	The current unprotected data window of a database. Statistic: Mean. Interval: 15 minutes. Only applicable for SI and RAC CDBs version 19c and later.
Shown as second
oci.oracle.oci.database.unusable.indexes
(gauge)	The number of unusable indexes in the database schema.
Shown as index
oci.oracle.oci.database.usable.fra
(gauge)	The usable fast recovery area.
Shown as percent
oci.oracle.oci.database.used.fraspace
(gauge)	The flash recovery area space usage.
Shown as gigabyte
oci.oracle.oci.database.user.calls
(count)	The combined number of logons, parses, and execute calls during the selected interval.
oci.oracle.oci.database.wait.time
(gauge)	The average rate of accumulation of non-idle wait time by foreground sessions in the database instance over the time interval. The wait time component of Average Active Sessions.
Shown as fraction
oci.oracle.oci.database.dbmgmt.job.executions.count
(count)	The number of SQL job executions on a single Managed Database or a Database Group, and their status.
Shown as execution
oci.fastconnect.bits.received
(count)	Number of bits received on the FastConnect interface at the Oracle end of the connection. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as bit
oci.fastconnect.bits.sent
(count)	Number of bits sent from the FastConnect interface at the Oracle end of the connection. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as bit
oci.fastconnect.bytes.received
(count)	Number of bytes received on the FastConnect interface at the Oracle end of the connection. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as byte
oci.fastconnect.bytes.sent
(count)	Number of bytes sent from the FastConnect interface at the Oracle end of the connection. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as byte
oci.fastconnect.connection.state
(gauge)	The values are up (1) or down (0). For a virtual circuit, the operational state of the virtual circuit's interface. For a cross-connect group, this reflects the overall operational state of the cross-connects that make up the cross-connect group (LAG). If at least one of the cross-connects is up, this value is up (1). If all the cross-connects in the group are down, this value is down (0).
oci.fastconnect.ipv.4bgp.session.state
(gauge)	The values are up (1) or down (0). The status of the IPv4 BGP session for a virtual circuit.
oci.fastconnect.ipv.6bgp.session.state
(gauge)	The values are up (1) or down (0). The status of the IPv6 BGP session for a virtual circuit.
oci.fastconnect.packets.discarded
(count)	Number of packets discarded at the Oracle end of the connection.
Shown as packet
oci.fastconnect.packets.error
(count)	Number of packets dropped at the Oracle end of the connection. Dropped packets indicate a misconfiguration in some part of the overall system. Check if there's been a change to the configuration of your VCN, the virtual circuit, or your CPE. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as packet
oci.fastconnect.packets.received
(count)	Number of packets received on the FastConnect interface at the Oracle end of the connection. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as packet
oci.fastconnect.packets.sent
(count)	Number of packets sent from the FastConnect interface at the Oracle end of the connection. For a cross-connect group (LAG), the value is the sum across all cross-connects in the group.
Shown as packet
oci.filestorage.file.system.read.average.latency.by.size
(gauge)	Read latency by size. Expressed as average read latency per second, grouped by size.
Shown as second
oci.filestorage.file.system.read.requests.by.size
(gauge)	Read requests by size. Expressed as operation per second, grouped by size.
Shown as operation
oci.filestorage.file.system.read.throughput
(count)	Read throughput for the file system. If the file system is exported through multiple mount targets, total throughput for all mount targets is displayed. Expressed as bytes read per second.
Shown as byte
oci.filestorage.file.system.usage
(gauge)	Total space utilization for a file system. Expressed as GiB consumed per second.
Shown as byte
oci.filestorage.file.system.write.average.latency.by.size
(gauge)	Write latency by size. Expressed as average write latency per second, grouped by size.
Shown as second
oci.filestorage.file.system.write.requests.by.size
(count)	Write requests by size. Expressed as operation per second, grouped by size.
Shown as operation
oci.filestorage.file.system.write.throughput
(count)	Write throughput for the file system. If the file system is exported through multiple mount targets, total throughput for all mount targets is displayed. Expressed as bytes written per second.
Shown as byte
oci.filestorage.kerberos.errors
(count)	Kerberos errors seen by the mount target while receiving IO from an NFS client. Expressed as a sum of errors per interval.
Shown as error
oci.filestorage.ldap.connection.errors
(count)	Connection failures between mount targets and the LDAP server for this outbound connector. Expressed as error count by error type per interval.
Shown as error
oci.filestorage.ldap.request.average.latency
(gauge)	Mount target to LDAP server request latency for this outbound connector. Expressed as mean latency, in seconds, by request type.
Shown as second
oci.filestorage.ldap.request.errors
(count)	LDAP query failures over an established connection between mount targets and the LDAP server for this outbound connector. Expressed as error count by error type per interval.
Shown as error
oci.filestorage.ldap.request.throughput
(count)	Requests from the mount target to the LDAP server through its outbound connector. Expressed as request type and outbound connector per interval.
Shown as request
oci.filestorage.metadata.iops
(gauge)	IOPs (Input/Output Operations Per Second) for the following NFS operations: CREATE, GETATTR, SETATTR, and REMOVE. Expressed as operations per second.
Shown as operation
oci.filestorage.metadata.request.average.latency
(gauge)	Average metadata request latency for the following NFS operations: CREATE, GETATTR, SETATTR, and REMOVE. Expressed as average latency per second, grouped by operation.
Shown as second
oci.filestorage.mount.target.connections
(count)	Number of client connections for the mount target. Expressed as total connection count at the interval.
Shown as connection
oci.filestorage.mount.target.health
(gauge)	Number of successfully executed NFS API requests. Expressed as a percentage of total requests per interval.
Shown as percent
oci.filestorage.mount.target.read.throughput
(count)	Read throughput for the mount target. If the mount target exports multiple file systems, total throughput for all file systems is displayed. Expressed as bytes read per interval.
Shown as byte
oci.filestorage.mount.target.write.throughput
(count)	Write throughput for the mount target. If the mount target exports multiple file systems, total throughput for all file systems is displayed. Expressed as bytes written per interval.
Shown as byte
oci.filestorage.replication.egress.throughput
(count)	Data that has been copied out of the source region. Only applicable for cross-region replication. Expressed as a sum of bytes written per interval.
Shown as byte
oci.filestorage.replication.recovery.point.age
(gauge)	Age of the last fully copied snapshot that was applied to the target file system. Or, how much older the data on the target file system is than the source file system. Expressed as time since the source snapshot was taken. Monitor this metric to ensure that the data on the target file system isn't older than your requirements allow (RPO).
Shown as time
oci.filestorage.replication.throughput
(count)	Throughput of the data transferred out of the source file system. Expressed as bytes read per interval.
Shown as byte
oci.faas.allocated.provisioned.concurrency
(gauge)	Memory consumed by provisioned concurrency slots.
Shown as megabyte
oci.faas.allocated.total.concurrency
(gauge)	Total concurrent memory allocated.
Shown as megabyte
oci.faas.function.execution.duration
(count)	Total function execution duration. Expressed in milliseconds.
Shown as millisecond
oci.faas.function.invocation.count
(count)	Total number of function invocations.
oci.faas.function.response.count
(count)	Total number of function responses.
Shown as invocation
oci.lbaas.accepted.connections
(count)	The number of connections accepted by the load balancer.
Shown as connection
oci.lbaas.accepted.sslhandshake
(count)	The number of accepted SSL handshakes.
Shown as operation
oci.lbaas.active.connections
(count)	The number of active connections from clients to the load balancer.
Shown as connection
oci.lbaas.active.sslconnections
(count)	The number of active SSL connections.
Shown as connection
oci.lbaas.backend.servers
(gauge)	The number of backend servers in the backend set.
Shown as instance
oci.lbaas.backend.timeouts
(count)	The number of timeouts across all backend servers.
Shown as timeout
oci.lbaas.bytes.received
(count)	The number of bytes received by the load balancer.
Shown as byte
oci.lbaas.bytes.sent
(count)	The number of bytes sent across all backend servers.
Shown as byte
oci.lbaas.closed.connections
(count)	The number of connections closed between the load balancer and backend servers.
Shown as connection
oci.lbaas.failed.sslclient.cert.verify
(count)	The number of failed client SSL certificate verifications.
Shown as error
oci.lbaas.failed.sslhandshake
(count)	The number of failed SSL handshakes.
Shown as error
oci.lbaas.handled.connections
(count)	The number of connections handled by the load balancer.
Shown as connection
oci.lbaas.http.requests
(count)	The number of incoming client requests to the backend set.
Shown as request
oci.lbaas.http.responses
(count)	The number of HTTP responses across all backend servers.
Shown as response
oci.lbaas.http.responses.200
(count)	The number of HTTP 200 responses received from backend sets.
Shown as response
oci.lbaas.http.responses.2xx
(count)	The number of HTTP 2xx responses received from backend sets.
Shown as response
oci.lbaas.http.responses.3xx
(count)	The number of HTTP 3xx responses received from backend sets.
Shown as response
oci.lbaas.http.responses.4xx
(count)	The number of HTTP 4xx responses received from backend sets.
Shown as response
oci.lbaas.http.responses.502
(count)	The number of HTTP 502 responses received from backend sets.
Shown as response
oci.lbaas.http.responses.504
(count)	The number of HTTP 504 responses received from backend sets.
Shown as response
oci.lbaas.http.responses.5xx
(count)	The number of HTTP 5xx responses received from backend sets.
Shown as response
oci.lbaas.http.responses.200
(count)	The number of HTTP 200 responses received from backend servers.
Shown as response
oci.lbaas.http.responses.2xx
(count)	The number of HTTP 2xx responses received from backend servers.
Shown as response
oci.lbaas.http.responses.3xx
(count)	The number of HTTP 3xx responses received from backend servers.
Shown as response
oci.lbaas.http.responses.4xx
(count)	The number of HTTP 4xx responses received from backend servers.
Shown as response
oci.lbaas.http.responses.502
(count)	The number of HTTP 502 responses received from backend servers.
Shown as response
oci.lbaas.http.responses.504
(count)	The number of HTTP 504 responses received from backend servers.
Shown as response
oci.lbaas.http.responses.5xx
(count)	The number of HTTP 5xx responses received from backend servers.
Shown as response
oci.lbaas.invalid.header.responses
(count)	The number of invalid header responses across all backend servers.
Shown as response
oci.lbaas.keep.alive.connections
(count)	The number of keep-alive connections.
Shown as connection
oci.lbaas.peak.bandwidth
(gauge)	Maximum bits per second bandwidth used during the specified interval.
Shown as bit
oci.lbaas.response.time.first.byte
(gauge)	Average time to the first byte of response from backend servers. TCP only.
Shown as millisecond
oci.lbaas.response.time.http.header
(gauge)	Average response time of backend servers. HTTP only.
Shown as millisecond
oci.lbaas.unhealthy.backend.servers
(gauge)	The number of unhealthy backend servers in the backend set.
Shown as instance
oci.mysql.database.active.connections
(gauge)	The number of connections actively executing statements against the MySQL DB system.
Shown as connection
oci.mysql.database.backup.failure
(gauge)	Backup failure events observed over the last interval. 0 - OK 1 - FAILED
oci.mysql.database.backup.size
(gauge)	The aggregate size of all backups per DB system.
Shown as byte
oci.mysql.database.backup.time
(gauge)	The time taken to create a backup.
Shown as millisecond
oci.mysql.database.cpuutilization
(gauge)	CPU utilization for the MySQL DB system host or HeatWave nodes.
Shown as percent
oci.mysql.database.channel.failure
(gauge)	The channel health status observed over the last interval. One of the following values: 0 - HEALTHY 1 - FAILED To troubleshoot inbound replication failure, see Troubleshooting Inbound Replication.
oci.mysql.database.channel.lag
(gauge)	The channel lag, with respect to the immediate source of the channel, observed over the last interval. If the channel is configured with replication delay, the channel lag includes the replication delay. See Creating a Replication Channel.
Shown as millisecond
oci.mysql.database.current.connections
(gauge)	The number of current connections to the MySQL DB system.
Shown as connection
oci.mysql.database.db.volume.read.bytes
(count)	The total bytes read from the MySQL DB system volume(s).
Shown as byte
oci.mysql.database.db.volume.read.operations
(count)	The total number of read operations for the DB volume(s).
Shown as operation
oci.mysql.database.db.volume.utilization
(gauge)	The total space utilization of the MySQL DB system volume(s).
Shown as percent
oci.mysql.database.db.volume.write.bytes
(count)	The total bytes written to the MySQL DB system volume(s).
Shown as byte
oci.mysql.database.db.volume.write.operations
(count)	The total number of write operations for the MySQL DB volume(s).
Shown as operation
oci.mysql.database.heat.wave.data.load.progress
(gauge)	Progress of data load into HeatWave cluster memory.
Shown as percent
oci.mysql.database.heat.wave.health
(gauge)	HeatWave cluster health status. One of the following values: 0 - HEALTHY 0.5: RELOADING DATA 1 - RECOVERING 2 - FAILED See HeatWave Cluster Failure and Recovery.
oci.mysql.database.heat.wave.statements
(count)	The number of statements executed against the MySQL DB System and were executed on HeatWave cluster.
oci.mysql.database.memory.allocated
(gauge)	The total amount of memory allocated during the selected interval.
Shown as gigabyte
oci.mysql.database.memory.used
(gauge)	The maximum amount of memory used during the selected interval.
Shown as gigabyte
oci.mysql.database.memory.utilization
(gauge)	Memory utilization for the MySQL DB system host or HeatWave nodes.
Shown as percent
oci.mysql.database.network.receive.bytes
(count)	Network receive bytes for the MySQL DB system.
Shown as byte
oci.mysql.database.network.transmit.bytes
(count)	Network transmit bytes for the MySQL DB system.
Shown as byte
oci.mysql.database.ocpus.allocated
(gauge)	The actual number of OCPUs allocated during the selected interval.
oci.mysql.database.ocpus.used
(gauge)	The actual number of OCPUs used during the selected interval.
oci.mysql.database.statement.latency
(gauge)	Statement latency for all executed statements.
Shown as millisecond
oci.mysql.database.statements
(count)	The number of statements executed against the MySQL DB system.
oci.mysql.database.storage.allocated
(gauge)	The maximum amount of space allocated to the DB system during the interval.
Shown as gigabyte
oci.mysql.database.storage.used
(gauge)	The maximum amount of space used during the interval.
Shown as gigabyte
oci.nat.gateway.bytes.from.natgw
(count)	Number of bytes sent from NAT gateway to OCI resources.
Shown as byte
oci.nat.gateway.bytes.to.natgw
(count)	Number of bytes sent from Oracle Cloud Infrastructure (OCI) resources to NAT gateway.
Shown as byte
oci.nat.gateway.connections.closed
(count)	Number of connections via NAT gateway that were closed by the internet host
oci.nat.gateway.connections.established
(count)	Number of connections established via NAT gateway
oci.nat.gateway.connections.timed.out
(count)	Number of connections closed by NAT gateway due to idle time out
oci.nat.gateway.drops.to.natgw
(count)	Number of packets from OCI resources to NAT Gateway that were dropped by NAT Gateway.
Shown as packet
oci.nat.gateway.packets.from.natgw
(count)	Number of packets sent from NAT gateway to OCI resources.
Shown as packet
oci.nat.gateway.packets.to.natgw
(count)	Number of packets sent from OCI resources to NAT gateway.
Shown as packet
oci.objectstorage.all.requests
(count)	The total number of all HTTP requests made in a bucket. Emit frequency: every 100 ms
Shown as request
oci.objectstorage.client.errors
(count)	The total number of 4xx errors for requests made in a bucket. Emit frequency: every 100 ms
Shown as error
oci.objectstorage.enabled.olm
(gauge)	Indicates whether a bucket has any executable Object Lifecycle Management policies configured. EnabledOLM emits: 1 if policies are configured 0 if no policies are configured Emit frequency: every 3 hours
oci.objectstorage.first.byte.latency
(gauge)	The per-request time measured from the time Object Storage receives the complete request to when Object Storage returns the first byte of the response. Emit frequency: every 100 ms
Shown as millisecond
oci.objectstorage.object.count
(count)	The count of objects in the bucket, excluding any multipart upload parts that have not been discarded (aborted) or committed. Emit frequency: every hour
oci.objectstorage.post.requests
(count)	The total number of HTTP Post requests made in a bucket. Emit frequency: every 100 ms
Shown as request
oci.objectstorage.put.requests
(count)	The total number of PutObject requests made in a bucket. Emit frequency: every 100 ms
Shown as request
oci.objectstorage.stored.bytes
(gauge)	The size of the bucket, excluding any multipart upload parts that have not been discarded (aborted) or committed. Emit frequency: every hour
Shown as byte
oci.objectstorage.total.request.latency
(gauge)	The per-request time from the first byte received by Object Storage to the last byte sent from Object Storage. Emit frequency: every 100 ms
Shown as millisecond
oci.objectstorage.uncommitted.parts
(gauge)	The size of any multipart upload parts that have not been discarded (aborted) or committed. Emit frequency: every hour
Shown as byte
oci.oke.apiserver.request.count
(count)	Number of requests received by the Kubernetes API Server.
Shown as request
oci.oke.apiserver.response.count
(count)	Number of different non-200 responses (that is, error responses) sent from the Kubernetes API server.
Shown as response
oci.oke.kubernetes.node.condition
(gauge)	Number of worker nodes in different conditions, as indicated by the Kubernetes API server.
Shown as node
oci.oke.node.state
(gauge)	Number of compute nodes in different states.
Shown as node
oci.oke.unschedulable.pods
(gauge)	Number of pods that the Kubernetes scheduler is unable to schedule. Not available in clusters running versions of Kubernetes prior to version 1.15.x.
oci.queue.consumer.lag
(gauge)	Difference in time between the oldest message in the queue and the current time
Shown as minute
oci.queue.messages.count
(count)	Count of messages sent and received per queue
Shown as message
oci.queue.messages.in.queue.count
(gauge)	Count of messages in the queue
oci.queue.queue.size
(gauge)	Bytes in the queue
Shown as byte
oci.queue.request.success
(count)	Indicates the success of the requests sent and received per queue
oci.queue.requests.latency
(gauge)	Latency of the requests to the queue
Shown as millisecond
oci.queue.requests.throughput
(gauge)	Bytes sent and received per queue
Shown as byte
oci.service.connector.hub.bytes.read.from.source
(count)	Number of bytes read from the source. Note: This value is emitted each time Connector Hub reads data from the source. If failures occur at the task or destination and Connector Hub needs to reread data from the source, the value is emitted again.
Shown as byte
oci.service.connector.hub.bytes.read.from.task
(count)	Number of bytes moved from the task to Connector Hub.
Shown as byte
oci.service.connector.hub.bytes.written.to.target
(count)	Number of bytes written to the target. Note: Use this metric as a general indicator of success. BytesWrittenToTarget might not match BytesReadFromSource or BytesReadFromTask. For example, consider a 10MB read intended for an Object Storage target. Connector Hub might compress the data, converting 10MB read into 1MB written.
Shown as byte
oci.service.connector.hub.bytes.written.to.task
(count)	Number of bytes moved by Connector Hub to the task.
Shown as byte
oci.service.connector.hub.data.freshness
(gauge)	Indicates age of the oldest processed record of the most recent set.
Shown as millisecond
oci.service.connector.hub.errors.at.source
(count)	Number of errors that affect retrieving data from source. Tip: To troubleshoot errors, view the errorCode and errorType dimension values. For example, an errorCode value that starts with 5, such as 500, implies a partner service outage, while the errorCode value –1 implies a network outage or timeout.
Shown as error
oci.service.connector.hub.errors.at.target
(count)	Number of errors that affect writing data to target. Tip: To troubleshoot errors, view the errorCode and errorType dimension values. For example, an errorCode value that starts with 5, such as 500, implies a partner service outage, while the errorCode value –1 implies a network outage or timeout.
Shown as error
oci.service.connector.hub.errors.at.task
(count)	Number of errors while writing to the task. Tip: To troubleshoot errors, view the errorCode and errorType dimension values. For example, an errorCode value that starts with 5, such as 500, implies a partner service outage, while the errorCode value –1 implies a network outage or timeout.
Shown as error
oci.service.connector.hub.latency.at.source
(gauge)	Time-to-first-byte when retrieving data from source. Useful for customers to troubleshoot with complex tasks (log rules).
Shown as millisecond
oci.service.connector.hub.latency.at.target
(gauge)	Time-to-first-byte when writing data to target.
Shown as millisecond
oci.service.connector.hub.latency.at.task
(gauge)	Time-to-first-byte for task; includes latency reading from the source, errors at the task, and errors writing to the target.
Shown as millisecond
oci.service.connector.hub.messages.read.from.source
(count)	Number of records read from the source. Note: The value for this metric is cumulative.
Shown as message
oci.service.connector.hub.messages.read.from.task
(count)	Number of messages moved from the task to Connector Hub.
Shown as message
oci.service.connector.hub.messages.written.to.target
(count)	Number of records written to the target.
Shown as message
oci.service.connector.hub.messages.written.to.task
(count)	Number of messages moved by Connector Hub to the task.
Shown as message
oci.service.connector.hub.service.connector.hub.errors
(count)	Number of errors in Connector Hub that affect moving data from source to target.
Shown as error
oci.service.gateway.bytes.from.service
(count)	The number of bytes successfully sent from the service gateway toward customer instances.
Shown as byte
oci.service.gateway.bytes.to.service
(count)	The number of bytes successfully sent from the service gateway toward Oracle services.
Shown as byte
oci.service.gateway.packets.from.service
(count)	The number of packets successfully sent from the service gateway toward customer instances.
Shown as packet
oci.service.gateway.packets.to.service
(count)	The number of packets successfully sent from the service gateway toward Oracle services.
Shown as packet
oci.service.gateway.sgw.drops.from.service
(count)	The number of packets dropped while sending packets from the service gateway toward customer instances.
Shown as packet
oci.service.gateway.sgw.drops.to.service
(count)	The number of packets dropped while sending packets from the service gateway toward Oracle services.
Shown as packet
oci.vcn.smartnic.buffer.drops.from.host
(count)	Number of packets dropped in SmartNIC from host due to buffer exhaustion.
Shown as packet
oci.vcn.smartnic.buffer.drops.from.network
(count)	Number of packets dropped in SmartNIC from network due to buffer exhaustion.
Shown as packet
oci.vcn.vnic.conntrack.is.full
(gauge)	Boolean (0/false, 1/true) that indicates the connection tracking table is full.
oci.vcn.vnic.conntrack.util.percent
(gauge)	Total utilization percentage (0-100%) of the connection tracking table.
Shown as percent
oci.vcn.vnic.egress.drops.conntrack.full
(count)	Packets sent from the VNIC, destined for the network, dropped due to full connection tracking table.
Shown as packet
oci.vcn.vnic.egress.drops.security.list
(count)	Packets sent by the VNIC, destined for the network, dropped due to security rule violations.
Shown as packet
oci.vcn.vnic.egress.drops.throttle
(count)	Packets sent from the VNIC, destined for the network, dropped due to throttling.
Shown as packet
oci.vcn.vnic.from.network.bytes
(count)	Bytes received at the VNIC from the network, after drops.
Shown as byte
oci.vcn.vnic.from.network.packets
(count)	Packets received at the VNIC from the network, after drops.
Shown as packet
oci.vcn.vnic.ingress.drops.conntrack.full
(count)	Packets received from the network, destined for the VNIC, dropped due to full connection tracking table.
Shown as packet
oci.vcn.vnic.ingress.drops.security.list
(count)	Packets received from the network, destined for the VNIC, dropped due to security rule violations.
Shown as packet
oci.vcn.vnic.ingress.drops.throttle
(count)	Packets received from the network, destined for the VNIC, dropped due to throttling.
Shown as packet
oci.vcn.vnic.to.network.bytes
(count)	Bytes sent from the VNIC to the network, before drops.
Shown as byte
oci.vcn.vnic.to.network.packets
(count)	Packets sent from the VNIC to the network, before drops.
Shown as packet
oci.vpn.bytes.received
(count)	Number of bytes received at the Oracle end of the connection.
Shown as byte
oci.vpn.bytes.sent
(count)	Number of bytes sent from the Oracle end of the connection.
Shown as byte
oci.vpn.packets.error
(count)	Number of packets dropped at the Oracle end of the connection. Dropped packets indicate a misconfiguration in some part of the overall system. Check if there's been a change to the configuration of your VCN, Site-to-Site VPN, or your CPE.
Shown as packet
oci.vpn.packets.received
(count)	Number of packets received at the Oracle end of the connection.
Shown as packet
oci.vpn.packets.sent
(count)	Number of packets sent from the Oracle end of the connection.
Shown as packet
oci.vpn.tunnel.state
(gauge)	Whether the tunnel is up (1) or down (0).
oci.waf.bandwidth
(gauge)	Bandwidth rate calculated by dividing total data egress in a minute by 60.
Shown as byte
oci.waf.number.of.requests
(count)	The total number of requests serviced by the WAF.
Shown as request
oci.waf.number.of.requests.detected
(count)	The number of requests that triggered a detect (alert) for a WAF policy.
Shown as request
oci.waf.traffic
(gauge)	Data egress from the WAF (compressed by default) measured in one minute intervals.
Shown as byte
oci.postgresql.buffer.cache.hit.ratio
(gauge)	The percentage of pages found in the buffer cache without reading from disk.
Shown as percent
oci.postgresql.connections
(count)	The number of database connections.
Shown as connection
oci.postgresql.cpu.utilization
(gauge)	The CPU utilization expressed as a percentage. The utilization percentage is reported with respect to the number of CPUs the database is allowed to use, which is two times the number of OCPUs.
Shown as percent
oci.postgresql.deadlocks
(count)	The number of locks on a database row where two or more transactions are waiting for another transaction to give up a locked row.
Shown as lock
oci.postgresql.memory.utilization
(gauge)	The percentage of total RAM that's in use.
Shown as percent
oci.postgresql.read.iops
(gauge)	The number of reads per second.
Shown as read
oci.postgresql.read.latency
(gauge)	Read latency in milliseconds.
Shown as millisecond
oci.postgresql.read.throughput
(gauge)	Reads in kilobytes per second.
Shown as kilobyte
oci.postgresql.used.storage
(gauge)	The amount of storage used, expressed in GB.
Shown as gigabyte
oci.postgresql.write.iops
(gauge)	The number of writes per second.
Shown as write
oci.postgresql.write.latency
(gauge)	Write latency in milliseconds.
Shown as millisecond
oci.postgresql.write.throughput
(gauge)	Writes in kilobytes per second.
Shown as kilobyte
oci.network.firewall.byte.received.count
(count)	The number of bytes received through the firewall.
Shown as byte
oci.network.firewall.byte.sent.count
(count)	The number of bytes sent through the firewall.
Shown as byte
oci.network.firewall.decryption.rule.hit.count
(count)	The number of times a connection matches a decryption rule.
oci.network.firewall.icmp.fragment.attacks.count
(count)	The number of ICMP fragment attacks detected.
oci.network.firewall.ip.spoof.count
(count)	Number of IP spoof attacks detected.
oci.network.firewall.land.attacks.count
(count)	The number of land attacks detected.
oci.network.firewall.mac.spoof.count
(count)	The number of MAC spoof attacks detected.
oci.network.firewall.packet.drop.count
(count)	The number of packets dropped through the firewall.
Shown as packet
oci.network.firewall.packet.received.count
(count)	The number of packets received at the firewall from the network, after drops.
Shown as packet
oci.network.firewall.packet.received.in.error.count
(count)	Number of packets received through the firewall that have errors.
Shown as packet
oci.network.firewall.packet.sent.count
(count)	The number of packets sent from the firewall to the network, after drops.
Shown as packet
oci.network.firewall.ping.of.death.attacks.count
(count)	The number of ping of death attacks detected.
oci.network.firewall.security.rule.hit.count
(count)	The number of times a connection matches a security rule.
oci.network.firewall.teardrop.attacks.count
(count)	The number of teardrop attacks detected.
"""

"""
Script below parses through above text to output a dictionary of metric names
mapped to their metric types in a JSON file.
"""
metrics_mapping = {}
metric_name_pattern = r"^oci\.[a-zA-Z0-9\.]+$"
metric_type_pattern = r"\((gauge|count)\)"

lines = text.strip().split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if re.match(metric_name_pattern, line):
        metric_name = line

        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            match = re.search(metric_type_pattern, next_line)

            if match:
                metric_type = match.group(1)
                if metric_type == "count":
                    metrics_mapping[metric_name] = {
                        "metric_type": "sum",
                        "aggregationTemporality": 1
                    }

                    with open('delta_counters.json', 'r') as f:
                        delta_counters = json.load(f)

                        for delta_counter in delta_counters:
                            if delta_counter in metrics_mapping:
                                metrics_mapping[delta_counter]["aggregationTemporality"] = 2
                else:
                    metrics_mapping[metric_name] = {
                        "metric_type": "gauge"
                    }

# Write metrics_mapping dictionary to metrics_mapping.json
with open('metrics_mapping.json', 'w') as f:
    json.dump(metrics_mapping, f, indent=4) 