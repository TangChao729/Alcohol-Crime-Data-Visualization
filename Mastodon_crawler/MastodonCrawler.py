from mastodon import Mastodon, StreamListener
import queue

"""
A live crawling tool for Mastodon Server, with two input args:

1)  server_address
    Mastodon has multiple server and each server has different server_address: 
        mastodon.au
        mastodon.social
        ...
    input should be a string of mastodon server address

2)  server_token
    Each mastodon developer token is matching to a single server
    it can be get under user -> preferences -> developer -> application -> token

"""


class MastodonCrawler:

    """
    Initialize the MastodonCrawler with the server address and access token.
    """

    def __init__(self, server_address, server_token=None):
        self.server_address = server_address
        if server_token == "None":
            self.server_token = None
        else:
            self.server_token = server_token
        self.m = Mastodon(api_base_url=server_address, access_token=self.server_token)
        self.data_queue = queue.Queue()
        self.listeners = []
        self.streams = []
        print("Initializing Mastodon Crawler...")

    class Listener(StreamListener):
        def __init__(self, data_queue):
            super().__init__()
            self.data_queue = data_queue

        def on_update(self, status):
            self.data_queue.put(status)

    def start_crawling(self):
        public_listener = self.Listener(self.data_queue)
        public_stream = self.m.stream_public(public_listener, run_async=True)

        self.listeners.append(public_listener)
        self.streams.append(public_stream)

        if self.server_token:
            user_listener = self.Listener(self.data_queue)
            user_stream = self.m.stream_user(user_listener, run_async=True)
            self.listeners.append(user_listener)
            self.streams.append(user_stream)

        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.data_queue.get(timeout=5)
        except queue.Empty:
            print("\nQueue is empty, waiting for new data...")
            return None

    def stop_crawling(self):
        for stream in self.streams:
            stream.close()
