import json
import couchdb

with open("twitterConfiguration.json") as f:
    configuration = json.load(f)

map_fun = "function (doc) {emit(doc.author_id, doc.sentiment);}"

# define the reduce function
reduce_fun = "function (keys, values, rereduce) {return sum(values);}"

if __name__ == '__main__':

    address = f'http://admin:password@{configuration["couchdb_ip"]}:{configuration["couchdb_port"]}/'
    # connect to the CouchDB server
    server = couchdb.Server(address)
    db = server[configuration["couchdb_name"]]
    # define the map function

    # create the design document with the map function
    design_doc = {
        '_id': '_design/test1',
        'views': {
            'sentimentByAuthorid': {
                'map': map_fun,
                'reduce': reduce_fun,
            }
        }
    }

    # save the design document to the database
    db.save(design_doc)