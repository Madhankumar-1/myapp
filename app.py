from flask import Flask, request, jsonify
from datetime import datetime
import requests  # For making HTTP requests

app = Flask(__name__)

# In-memory data store
items = []

# Generate a unique instanceId based on the current time
def generate_instance_id():
    return f"inst-{int(datetime.now().timestamp() * 1000)}"


# Metadata service URL
METADATA_URL = "http://169.254.169.254/latest/meta-data"

# Step 1: Fetch the token
def fetch_token():
    try:
        response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},  # Token valid for 6 hours
            timeout=2
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token: {e}")
        return None

# Step 2: Fetch metadata using the token
def fetch_metadata(token, path):
    try:
        response = requests.get(
            f"{METADATA_URL}/{path}",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None

# Main function
def get_instance_ip_address():
    token = fetch_token()
    if not token:
        print("Failed to fetch token. Exiting.")
        return

    # Fetch the private IP address
    private_ip = fetch_metadata(token, "local-ipv4")
    if private_ip:
        print(f"Private IP Address: {private_ip}")
    else:
        print("Failed to fetch private IP address.")
    return private_ip


# Default route
@app.route('/', methods=['GET'])
def default_route():
    machine_id = get_instance_ip_address()
    response = {
        "instanceId": generate_instance_id(),
        "machineId": machine_id,
        "type": "python",  # Default type
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
    query_param = request.args
    message=query_param.get('message', default='none')
    machine_id = get_instance_ip_address()
    response = {
        "instanceId": generate_instance_id(),
        "machineId": machine_id,
        "type": "nodejs",  # Default type
        "deployment": "aws-ec2",  # Default deployment
        "pathParams": path_param,  # Path parameter
        "queryParams":  query_param,  # Query parameters
        "method": request.method,
        "path": request.path,
        "startTime": datetime.utcnow().isoformat() + "Z",
        "message": f"Hello World, Pathparam: {path_param}, Queryparam: {message}",
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



    import requests

# Metadata service URL
METADATA_URL = "http://169.254.169.254/latest/meta-data"

# Step 1: Fetch the token
def fetch_token():
    try:
        response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},  # Token valid for 6 hours
            timeout=2
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token: {e}")
        return None

# Step 2: Fetch metadata using the token
def fetch_metadata(token, path):
    try:
        response = requests.get(
            f"{METADATA_URL}/{path}",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None

# Main function
def main():
    token = fetch_token()
    if not token:
        print("Failed to fetch token. Exiting.")
        return

    # Fetch the private IP address
    private_ip = fetch_metadata(token, "local-ipv4")
    if private_ip:
        print(f"Private IP Address: {private_ip}")
    else:
        print("Failed to fetch private IP address.")


