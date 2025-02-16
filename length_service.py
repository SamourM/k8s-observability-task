from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/length', methods=['POST'])
def length_of_string():
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

        # Calculate length of string
        length = len(input_string)
        return jsonify({"length": length})

    except Exception as e:
        # Catch any unexpected errors and return a generic error message
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
