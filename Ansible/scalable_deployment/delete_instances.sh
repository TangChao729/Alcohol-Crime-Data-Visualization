#!/bin/bash

echo "Please type the name of the text file located at ./deployed directory:"
read filename

instance_names=()
while IFS= read -r line
do
    instance_name=${line%,*}  # extract instance name part before the comma
    [[ -n $instance_name ]] && instance_names+=("$instance_name")  # add only non-empty lines
done < "./deployed_ips/${filename}"

# Convert array to space-separated string
instance_names_string="${instance_names[@]}"
echo $instance_names_string
read -p "Press enter to confirm and proceed..."

# Execute Ansible playbook with instance names as extra-vars
. ./openrc.sh; ansible-playbook -vv delete_instances.yaml -e "instance_names=\"$instance_names_string\"" | tee ./outputs/delete.txt
