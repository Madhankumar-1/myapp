from flask import Flask, request, jsonify
from datetime import datetime
import requests  # For making HTTP requests

app = Flask(__name__)

# In-memory data store
items = []

# Generate a unique instanceId based on the current time
def generate_instance_id():
    return f"inst-{int(datetime.now().timestamp() * 1000)}"

# Fetch the EC2 instance's private IP address
def get_instance_ip_address():
    try:
        response = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=2)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching instance IP address: {e}")
        return "unknown"

# Default route
@app.route('/', methods=['GET'])
def default_route():
    machine_id = get_instance_ip_address()
    response = {
        "instanceId": generate_instance_id(),
        "machineId": machine_id,
        "type": "nodejs",  # Default type
        "deployment": "aws-ec2",  # Default deployment
        "pathParams": {},  # No path parameters
        "queryParams": {},  # No query parameters
        "method": request.method,
        "path": request.path,
        "startTime": datetime.utcnow().isoformat() + "Z",
        "message": "Hello World, Pathparam: none, Queryparam: none",
    }
    return jsonify(response)

# Route with path parameter
@app.route('/<path_param>', methods=['GET'])
def path_param_route(path_param):
    machine_id = get_instance_ip_address()
    response = {
        "instanceId": generate_instance_id(),
        "machineId": machine_id,
        "type": "nodejs",  # Default type
        "deployment": "aws-ec2",  # Default deployment
        "pathParams": {"pathParam": path_param},  # Path parameter
        "queryParams": {},  # No query parameters
        "method": request.method,
        "path": request.path,
        "startTime": datetime.utcnow().isoformat() + "Z",
        "message": f"Hello World, Pathparam: {path_param}, Queryparam: none",
    }
    return jsonify(response)

# Route with path parameter and query parameter
@app.route('/<path_param>/query', methods=['GET'])
def path_and_query_route(path_param):
    query_param = request.args.get('queryParam', default='none')
    machine_id = get_instance_ip_address()
    response = {
        "instanceId": generate_instance_id(),
        "machineId": machine_id,
        "type": "nodejs",  # Default type
        "deployment": "aws-ec2",  # Default deployment
        "pathParams": {"pathParam": path_param},  # Path parameter
        "queryParams": {"queryParam": query_param},  # Query parameters
        "method": request.method,
        "path": request.path,
        "startTime": datetime.utcnow().isoformat() + "Z",
        "message": f"Hello World, Pathparam: {path_param}, Queryparam: {query_param}",
    }
    return jsonify(response)

# CRUD Operations 
# Create (POST)
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    items.append(new_item)
    return jsonify(new_item), 201

# Read (GET all items)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Read (GET single item by ID)
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = next((i for i in items if i['id'] == id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404

# Update (PUT)
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    updated_item = request.json
    item = next((i for i in items if i['id'] == id), None)
    if item:
        item.update(updated_item)
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404

# Delete (DELETE)
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    global items
    items = [i for i in items if i['id'] != id]
    return '', 204

# Start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
