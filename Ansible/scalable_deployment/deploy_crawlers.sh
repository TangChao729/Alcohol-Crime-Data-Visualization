#!/usr/bin/env bash

# Set default values
default_n=1
default_server="https://mastodon.au"
default_ip="172.26.130.104"
default_db="mastodon_data"

# Prompt for number of instances
read -p "Enter the number of instances [$default_n]: " n
n=${n:-$default_n}

# Prompt for Mastodon server
read -p "Enter the Mastodon server [$default_server]: " server
server=${server:-$default_server}

# Prompt for database IP
read -p "Enter the database IP address [$default_ip]: " ip
ip=${ip:-$default_ip}

# Prompt for database name
read -p "Enter the database name [$default_db]: " db
db=${db:-$default_db}

# Verify Mastodon server format
if ! [[ $server =~ ^https://.+ ]]; then
    echo "Invalid format for Mastodon server. It should start with 'https://'."
    exit 1
fi

# Verify IP address format
if ! [[ $ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Invalid format for IP address. It should be in the form X.X.X.X."
    exit 1
fi

# Generate the instance names
instance_names=()
for ((i=1; i<=n; i++)); do
    server_formatted=${server#https://}
    server_formatted=${server_formatted//./_}
    instance_name="mastodon_crawler_$(printf "%02d" $i)_${server_formatted}_$(echo "$ip" | tr '.' '_')_$db"
    instance_names+=("$instance_name")
done

# Final confirmation prompt
echo "You are about to create the following instances:"
for instance_name in "${instance_names[@]}"; do
    echo "- $instance_name"
done
echo "Targeting the server $server, with database IP $ip and database name $db."
read -p "Press enter to confirm and proceed..."

instance_names_string="${instance_names[@]}"
echo $instance_names_string

. ./openrc.sh; ansible-playbook -vv -i ./inventory/hosts.ini deploy_crawlers.yaml \
-e "n=$n" \
-e "Server_to_crawl=$server" \
-e "CouchDB_IP=$ip" \
-e "Database=$db" \
-e "instance_names=\"$instance_names_string\"" \
| tee ./outputs/deploy.txt
