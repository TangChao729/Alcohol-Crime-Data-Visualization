from flask import jsonify
from flask_restful import Resource, request
import couchdb
import queue
import random

class Database_concierge(Resource):
    def __init__(self, address_list, database):
        address_list.append(address_list.pop(0))
        
        print("\nConnecting to databases:", address_list, "database:", database)
        self.databases = queue.Queue()

        # self health check
        for address in address_list:
            try:
                couchDB = couchdb.Server(address)
                if database in couchDB:
                    print("Successfully connected to:", address, "database:", database)
                    self.databases.put(couchDB[database])
                else:
                    address_list.remove(address)
                    print("Error, no such database in:", address)
            except (couchdb.http.PreconditionFailed, couchdb.ServerError):
                print("Connection failed for:", address)
    
    # get one doc from connected database
    def get(self, doc_id=None):
        if doc_id:
            result = None
            for cnt in range(self.databases.qsize()):
                database = self.databases.get()
                try:
                    result = database[doc_id]
                    if result:
                        return result, 200
                except couchdb.http.ResourceNotFound:
                    pass
                finally:
                    self.databases.put(database)
                
            return {"error": "Document not found"}, 404
        else:
            return {"error": "Please provide a doc_id"}, 400
    
    # get one view from connected database
    def view(self, view_name=None):
        if view_name:

            reduce = request.args.get('reduce', 'false').lower()
            group = request.args.get('group', 'false').lower()

            query_params = {
                'reduce': reduce == 'true',
                'group': group == 'true'
            }

            result = []
            for cnt in range(self.databases.qsize()):
                database = self.databases.get()
                try:
                    for row in database.view(view_name, **query_params):
                        result.append(row)
                    if len(result) > 0:
                        return jsonify(result), 200
                except couchdb.http.ResourceNotFound:
                    pass
                finally:
                    self.databases.put(database)
                
            return {"error": "View not found"}, 404
        else:
            return {"error": "Please provide a view_name"}, 400

    # query the database with a json object    
    def query(self, query=None):
        if query:
            result = []
            for cnt in range(self.databases.qsize()):
                database = self.databases.get()
                try:
                    docs = database.find(query)
                    result.extend([doc for doc in docs])
                    if result:
                        return jsonify(result), 200
                except couchdb.http.ResourceNotFound:
                    pass
                finally:
                    self.databases.put(database)
                
            return {"error": "Query failed"}, 404
        else:
            return {"error": "Please provide a correct query"}, 400

    def post(self):
        data = request.get_json()

        if data:
            success = False
            for cnt in range(self.databases.qsize()):
                database = self.databases.get()
                try:
                    doc_id, doc_rev = database.save(data)
                    success = True
                    if success:
                        return {"id": doc_id, "rev": doc_rev}, 201
                except couchdb.http.ResourceConflict:
                    pass
                finally:
                    self.databases.put(database)
            if not success:  # If after all databases, save wasn't successful, return an error
                return {"error": "Failed to save the document"}, 500
        else:
            return {"error": "No data provided"}, 400

    def put(self, doc_id):
        data = request.get_json()

        if data:
            if doc_id:
                success = False
                for cnt in range(self.databases.qsize()):
                    database = self.databases.get()
                    try:
                        existing_doc = database[doc_id]
                        existing_doc.update(data)
                        database[doc_id] = existing_doc
                        success = True
                        if success:
                            return {"result": "Document updated successfully"}, 200
                    except couchdb.http.ResourceNotFound:
                        pass
                    finally:
                        self.databases.put(database)
                if not success:    
                    return {"error": "Fail to update"}, 400
            else:
                return {"error": "No doc_id provided"}, 400
        else:
            return {"error": "No data provided"}, 400

    def delete(self, doc_id=None):
        if doc_id:
            success = False
            for cnt in range(self.databases.qsize()):
                database = self.databases.get()
                try:
                    doc = database[doc_id]
                    database.delete(doc)
                    success = True
                    if success:
                        return {"result": "Document deleted successfully"}, 200
                except couchdb.http.ResourceNotFound:
                    pass
                finally:
                    self.databases.put(database)
            if not success:    
                return {"error": "Document not found"}, 404
        else:
            return {"error": "Document ID is required"}, 400
