# Native couchDB setup

**Database is running directly on instance without docker support, this is within criteria: “The CouchDB setup may be a single node or based on a clustered setup”**

## Prepare instance

First job is to mount volume to instance by:

1.  Attach volume to instance in MRC
    
2.  Check volume in instance by: sudo fdisk -l

3.  Format volume: sudo mkfs.ext4 /dev/vdb

4.  Mount volume to mounting point: sudo mount /dev/vdb /mnt_point

5.  Add this: /dev/vdb /mnt_point ext4 defaults 0 1 to /etc/fstab

6.  Grant access permission: sudo chown -R {user}:{user} /mnt_point | sudo chown -R 755 /mnt_point

Now you should have access permission to volume.

## Install couchDB

the official way is to following this guide:  
[https://docs.couchdb.org/en/stable/install/unix.html#installation-from-source](https://docs.couchdb.org/en/stable/install/unix.html#installation-from-source)

Before end, it will pop up a window to show configurable content such as admin password, local address or global, etc.
Use this command to start service: sudo systemctl start couchdb
Check service status by, if it is active, it is all good: sudo status couchdb
We can now access couchdb Fauxton by going to {ad.dr.es.s}:5984/_utils

## Config couchDB

configure couchDB to use the attached volume as the database storage.
We need to change the local.ini file of couchDB, it should be at /opt/couchdb/etc/local.ini
Adding “database_dir = /mnt_point” to the ini file and restart the service.
Access the address again. If not success, check error log.
Dont forget to grant couchdb as the user to have permission to access mnt_point



# Docker couchDB setup (single)


1. Mount attached volume same as above.

2. Install docker on ubuntu

* Pull docker couchDB image:

	> docker pull couchdb

 * Create directory to save database data:

	> mkdir -p /path/to/your/data

* Give permission to couchdb in docker container, typically, the UID and GID are both 5984 for the CouchDB user in the container.

	> sudo chown -R 5984:5984 /path/to/your/data

  

3. Run container:

	> docker run -d --name my-couchdb \

	> -p 5984:5984 \

	> -v /path/to/your/data:/opt/couchdb/data \

	> -e COUCHDB_USER=admin \

	> -e COUCHDB_PASSWORD=your-password \

	> couchdb

This should run a couchDB service on a docker container, you can access to this database as usual using 5984 port.



# Docker couchDB setup (cluster)


1. For each node:

	Create keypair on MRC
	Create instance on MRC, bind with keypair, security groups
	Create volume on MRC, attach to instance
    chmod 600 keypair.pem file on working pc, so can access via ssh

2. ssh to instance

	> sudo mkfs.ext4 /dev/vdb
		sudo mkdir -p /mnt/my_volume
		sudo mount /dev/vdb /mnt/my_volume
		sudo nano /etc/fstab # adding “/dev/vdb /mnt/my_volume ext4 defaults,nofail 0 0”
		sudo chown -R root:root /mnt/my_volume
		sudo chown -R 755 /mnt/my_volume
		sudo chown -R ubuntu:ubuntu /mnt/my_volume
		mkdir -p /mnt/my_volume/couch_database
		sudo chown -R 5984:5984 /mnt/my_volume/couch_database

3. Install docker by following above instruction
4. Now you can start docker container with these command

	> sudo docker run -d --name my-couchdb \
		--network host \
		-v /mnt/my_volume/couch_database:/opt/couchdb/data \
		-e COUCHDB_USER=admin \
		-e COUCHDB_PASSWORD=your-password \
		-e NODENAME=172.26.130.104 \
		-e ERL_FLAGS="-setcookie couchdb_cluster -name couchdb@172.26.130.104" \
		couchdb

	 >  **--network host make sure that docker will be communicable through IP address**

5. Config cluster by:  

	> curl -X POST -H "Content-Type: application/json" http://admin:your-password@localhost:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address": "0.0.0.0", "username": "admin", "password": "your-password", "port": 5984, "node_count": "3"}'

	  > curl -X POST -H "Content-Type: application/json" http://admin:your-password@localhost:5984/_cluster_setup -d '{"action": "add_node", "host": "172.26.129.208", "port": 5984, "username": "admin", "password": "your-password"}'

	  > curl -X POST -H "Content-Type: application/json" http://admin:your-password@localhost:5984/_cluster_setup -d '{"action": "add_node", "host": "172.26.132.73", "port": 5984, "username": "admin", "password": "your-password"}'

	  > curl -X POST -H "Content-Type: application/json" http://admin:your-password@localhost:5984/_cluster_setup -d '{"action": "finish_cluster"}'

  
6. Finally, you can check it with:  
	> curl -X GET -H "Content-Type: application/json" http://admin:your-password@localhost:5984/_membership