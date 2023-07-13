# Mastodon_crawler

Three py files are used:

1. JSONuploader.py this is used to directly store data using couchdb python lib. Parameters including server address, port num, admin and password.

2. MastodonCrawler.py this is used to connect to mastodon using API and dynamically monitoring new toots. It is then output to a generator.

3. Crawler.py this is the main file to be called. In which it import above two py file and call them respectively. We provide configurable information here.

To setup crawler on docker, we need below files in one directory, for example
mastodon_crawler_app
/mastodon_crawler_app/JSONuploader.py
/mastodon_crawler_app/MastodonCrawler.py
/mastodon_crawler_app/Crawler.py
/mastodon_crawler_app/requirements.txt
/mastodon_crawler_app/Dockerfile
/mastodon_crawler_app/docker-compose.yaml

## requirements.txt:

None

## Dockerfile:

#Use the official Python base image
FROM python:3.9

#Set the working directory
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt .

#Install any necessary dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Copy the rest of the application code
COPY . .

#Expose the port the app will run on
EXPOSE 8080

#Use environment variables for server, token and database
ENV SERVER_URL=""
ENV TOKEN=""
ENV DATABASE_NAME=""

#Define the command to run the application
CMD python StartCrawling.py -server $SERVER_URL -token $TOKEN -database $DATABASE_NAME

## docker-compose.yaml:

version: "3.8"
services:
mastodon-crawler:
build: .
container_name: mastodon
restart: always
environment: - SERVER_URL=https://mastodon.au - TOKEN=oGi9Wei1yWjj2LGgoRXRJMmKP7gqg0SmWztY7wVwEPc or None - DATABASE_NAME=m2

**With above set up ready, we can now run crawler.py on docker:**
sudo docker build -t crawler .
sudo docker run -d -e SERVER_URL=mastodon.world -e Token=None -e DATABASE_NAME=mastodon_all mastodon_crawler

or simply

sudo docker compose up
