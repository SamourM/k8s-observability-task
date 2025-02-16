from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/hash', methods=['POST'])
def hash_string():
    try:
        # Get the input data
        data = request.get_json()
        
        # Validate input
        if not data or 'text' not in data:
            return jsonify({"error": "Bad Request: 'text' field is required"}), 400

        input_string = data['text']

        # Check if input is a string
        if not isinstance(input_string, str):
            return jsonify({"error": "Bad Request: Input should be a string"}), 400

        # Generate the SHA256 hash
        hash_object = hashlib.sha256(input_string.encode())
        hash_hex = hash_object.hexdigest()

        return jsonify({"hash": hash_hex})

    except Exception as e:
        # Catch any unexpected errors and return a generic error message
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
