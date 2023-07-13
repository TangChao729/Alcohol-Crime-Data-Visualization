#!/usr/bin/env bash

# Final confirmation prompt
echo ""
echo "You are about to create the following a full-service over two instances:"
echo ""
echo "The first instance include CouchDB and Mastodon Crawling service"
echo "CouchDB image: couchdb" 
echo "Mastodon Crawler image: taytang91/mastodon_sentiment"
echo ""
echo "The second instance include frontend and backend service"
echo "Frontend image: taytang91/frontend_190523" 
echo "Backend image: taytang91/frontend_180523"
echo ""
read -p "Press enter to confirm and proceed..."

. ./openrc.sh; ansible-playbook -vv -i hosts mastodon_crawler.yaml | tee output.txt
