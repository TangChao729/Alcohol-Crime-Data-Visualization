from MastodonCrawler import MastodonCrawler
from JSONuploader import JSONuploader
import json
from datetime import datetime
import time
import argparse
from mastodon.errors import MastodonNetworkError
from SentimentAnalysis import SentimentAnalyzer

# Set up argument parser for mastodon crawling
parser = argparse.ArgumentParser(description="Start the Mastodon Crawler.")

# mastodon server and token
parser.add_argument("-server", type=str, help="Server address")
parser.add_argument("-token", type=str, help="Server token")

# saved to which database on couchDB
parser.add_argument("-c1", type=str, help="couchdb address")
parser.add_argument("-c2", type=str, help="couchdb port")
parser.add_argument("-c3", type=str, help="couchdb username")
parser.add_argument("-c4", type=str, help="couchdb password")
parser.add_argument("-database", type=str, help="Database name")

args = parser.parse_args()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


def go_fetch_me_data(args):
    # access to mastodon.au with Taylor's token
    # server_address = 'https://mastodon.au'
    # server_token = 'oGi9Wei1yWjj2LGgoRXRJMmKP7gqg0SmWztY7wVwEPc'
    # database_name = 'mastodon_crawling_data'
    server_address = args.server
    server_token = args.token
    crawler = MastodonCrawler(server_address, server_token).start_crawling()
    analyzer = SentimentAnalyzer()
    database_name = args.database
    servers = []
    if args.c1 != None and args.c2 != None and args.c3 != None and args.c4 != None:
        if args.c1 != "None" and args.c2 != "None" and args.c3 != "None" and args.c4 != "None":
            server = (args.c1, args.c2, args.c3, args.c4)
            servers.append(server)
            print("Connecting to custom couchdb server: ", server)

        else:
            server_1 = ("172.26.130.104", "5984", "admin", "your-password")
            server_2 = ("172.26.129.208", "5984", "admin", "your-password")
            server_3 = ("172.26.132.73", "5984", "admin", "your-password")
            servers.append(server_1)
            servers.append(server_2)
            servers.append(server_3)
            print("Connecting to default couchdb server: ", servers)

    else:
        server_1 = ("172.26.130.104", "5984", "admin", "your-password")
        server_2 = ("172.26.129.208", "5984", "admin", "your-password")
        server_3 = ("172.26.132.73", "5984", "admin", "your-password")
        servers.append(server_1)
        servers.append(server_2)
        servers.append(server_3)
        print("Connecting to default couchdb server: ", servers)

    js_uploader = JSONuploader(servers)

    # Continuously crawl data
    while True:
        # Get data from the generator
        retry_attempts = 3
        retry_interval = 5  # Time in seconds to wait before retrying

        for attempt in range(retry_attempts):
            try:
                data = next(crawler)
                break  # If the request is successful, break out of the loop
            except MastodonNetworkError as e:
                print(f"Network error occurred: {e}")
                if attempt < retry_attempts - 1:
                    print(f"Retrying in {retry_interval} seconds...")
                    time.sleep(retry_interval)
                else:
                    print(f"Request failed after {retry_attempts} attempts.")
        if data:
            json_str = json.dumps(data, cls=DateTimeEncoder)
            toot = json.loads(json_str)

            print("analyzing toot: ", toot["content"][:40], "...")
            if(analyzer.processMastodon(toot)):
                print(toot)
                js_uploader.upload(database_name, toot)
            # js_uploader.upload(database_name, toot)
        else:
            # Add a sleep time to avoid busy waiting
            print("Waiting...")
            time.sleep(5)

print("server", args.server)
print("token", args.token)
print("c1", args.c1)
print("c2", args.c2)
print("c3", args.c3)
print("c4", args.c4)
print("database", args.database)
go_fetch_me_data(args)
