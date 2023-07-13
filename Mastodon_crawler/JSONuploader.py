import couchdb
from couchdb.http import ResourceNotFound
import json
from concurrent.futures import ThreadPoolExecutor


class JSONuploader:
    def __init__(self, servers):
        self.couch_servers = []

        for server_info in servers:
            address, port, admin, password = server_info
            full_address = f"http://{admin}:{password}@{address}:{port}/"
            try:
                couch_server = couchdb.Server(full_address)
                status, headers, server_info_json = couch_server.resource.get()
                server_info = json.loads(server_info_json.read().decode("utf-8"))
                print(
                    f"Connected to server: {address}, CouchDB version: {server_info['version']}"
                )
                self.couch_servers.append(couch_server)
            except ResourceNotFound as e:
                print(f"Failed to connect to server: {address}. Error: {e}")

        self.total_server = len(self.couch_servers)
        self.curr_server = 0

        if self.total_server == 0:
            raise ValueError(
                "No CouchDB servers available. Please check the server configuration."
            )

    def upload(self, database_name, json_object, update=False):
        if self.total_server == 0:
            raise ValueError(
                "No CouchDB servers available. Please check the server configuration."
            )

        couch_server = self.couch_servers[self.curr_server]

        if database_name not in couch_server:
            database = couch_server.create(database_name)
        else:
            database = couch_server[database_name]

        id = str(json_object.get("id"))
        json_object["_id"] = id
        json_object.pop("id")

        # if specify id
        if id != "None":
            # for loop to prevent error from multithread
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # check if database contains object
                    if database.get(id):
                        # if update is required, update the object
                        if update == True:
                            rev = database.get(id).rev
                            json_object["_rev"] = rev
                            doc_id, doc_rev = database.save(json_object)
                            print(f"Updated: Doc ID: {doc_id} and rev {doc_rev}")

                        # else, ignore upload request
                        else:
                            # print(json_object["content"])
                            print(
                                "File already exist on database, consider update() object.\n"
                            )
                            pass

                    # if database doesn't contain object, upload it with specified id
                    else:
                        # json_object["_id"] = id
                        doc_id, doc_rev = database.save(json_object)
                        print(f"Saved: Doc ID: {doc_id} and rev {doc_rev}")

                    break

                # catch multithread error
                except couchdb.http.ResourceConflict:
                    if attempt < max_retries - 1:
                        print(f"Conflict on update attempt {attempt + 1}. Retrying...")
                        continue
                    else:
                        print(f"Update failed after {max_retries} attempts.")

        # if database doesn't contain object, upload with auto assigned id
        else:
            doc_id, doc_rev = database.save(json_object)
            print(f"Direct Saved: Doc ID: {doc_id} and rev {doc_rev}")

        self.curr_server = (self.curr_server + 1) % self.total_server

    def upload_batch(self, database_name, json_objects):
        if self.total_server == 0:
            raise ValueError(
                "No CouchDB servers available. Please check the server configuration."
            )

        with ThreadPoolExecutor(max_workers=self.total_server) as executor:
            results = executor.map(
                lambda obj: self.upload(database_name, obj),
                json_objects,
            )
        return list(results)

    def update(self, database_name, json_object, id):
        if self.total_server == 0:
            raise ValueError(
                "No CouchDB servers available. Please check the server configuration."
            )

        couch_server = self.couch_servers[self.curr_server]

        if database_name not in couch_server:
            database = couch_server.create(database_name)
        else:
            database = couch_server[database_name]

        if database.get(id):
            rev = database.get(id).rev
            json_object["_rev"] = rev

        doc_id, doc_rev = database.save(json_object)
        self.curr_server = (self.curr_server + 1) % self.total_server
        print(f"Updated: Doc ID: {doc_id} and rev {doc_rev}")

    def list_all_docs(self, database_name):
        if self.total_server == 0:
            raise ValueError(
                "No CouchDB servers available. Please check the server configuration."
            )

        couch_server = self.couch_servers[self.curr_server]

        if database_name not in couch_server:
            print("No such a database")
        else:
            database = couch_server[database_name]

        for _id in database:
            doc = database.get(_id)
            print(f"List: ID: {_id} and rev {doc['_rev']}")

        self.curr_server = (self.curr_server + 1) % self.total_server
