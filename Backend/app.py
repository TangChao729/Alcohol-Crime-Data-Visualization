print("Script started")

from flask import Flask, render_template, request, jsonify

print("Flask imported")

from flask_restful import Api

print("flask_restful imported")

from database_concierge import Database_concierge

print("database_concierge imported")

from flask import Flask

print("Flask imported again")

from flask_cors import CORS

print("flask_cors imported")

import os

print("os imported")

address_port_str = os.environ.get("DATABASE_ADDRESS") or "172.26.130.104:5984,172.26.129.208:5984,172.26.132.73:5984"
address_port = address_port_str.split(',')

port = os.environ.get("DATABASE_PORT") or 5984
print("port set")

admin = os.environ.get("DATABASE_USERNAME") or "admin"
print("admin set")

password = os.environ.get("DATABASE_PASSWORD") or "your-password"
print("password set")

address_list_full = [f"http://{admin}:{password}@{ap}/" for ap in address_port]
print("address set")

app = Flask(__name__)
print("app created")

api = Api(app)
print("api created")

CORS(app, origins="*")
print("CORS set")

# full_address = f"http://{admin}:{password}@{address}:{port}/"
# print("full_address set")

print("Starting service...")
print("Connecting to: ", address_list_full)


@app.route("/")
def home():
    return render_template("Index.html")


@app.route("/<database_name>", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<database_name>/<id>", methods=["GET", "PUT", "DELETE"])
def handle_request(database_name, id=None):
    try:
        mastodon_data = Database_concierge(address_list_full, database_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if request.method == "GET":
        return mastodon_data.get(doc_id=id)
    elif request.method == "POST":
        return mastodon_data.post()
    elif request.method == "PUT":
        return mastodon_data.put(doc_id=id)
    elif request.method == "DELETE":
        return mastodon_data.delete(doc_id=id)


@app.route("/<database_name>/view/<design_doc_name>/<view_name>", methods=["GET"])
def handle_view(database_name, design_doc_name, view_name):
    try:
        mastodon_data = Database_concierge(address_list_full, database_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return mastodon_data.view(f"{design_doc_name}/{view_name}")


@app.route("/<database_name>/query", methods=["POST"])
def handle_query(database_name):
    try:
        mastodon_data = Database_concierge(address_list_full, database_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    data = request.get_json()
    if data and "query" in data:
        return mastodon_data.query(data["query"])
    else:
        return {"error": "No query provided"}, 400


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port="8080")
