# Data exfiltration over MySQL protocol

The mysql server is requesting a file from the mysql client, this file contains a wealth of information on the client, unfortunatly this is feature abuse as blogged about here: https://www.percona.com/blog/2019/02/06/percona-responds-to-mysql-local-infile-security-issues/

The incident.pcap shows this, look to see what file path the server requests and what the client responds with.

