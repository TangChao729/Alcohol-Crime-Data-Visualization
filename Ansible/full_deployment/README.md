first download OpenStack RC file from MRC
reset and download password on MRC
run "run-crawler.sh"
paste password

MRC could fail on create instance, if so, delete and try again

this playbook do two things:

1. set up related resources for creating an instance, then create the instance
2. use created instance, to deploy services on it

regarding #1 
it set up volume, security group, and apply them to instance.

regarding #2
it first install dependencies, then install docker, and pull the image to deploy on docker