from flask import Flask, jsonify, request
from flask_cors import CORS
import snowflake.connector
import anthropic
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def get_connection():
    return snowflake.connector.connect(
        account=os.environ.get("SF_ACCOUNT", "bljdbql-ueb08426"),
        user=os.environ.get("SF_USER", "your_username"),
        password=os.environ.get("SF_PASSWORD", "your_password"),
        warehouse=os.environ.get("SF_WAREHOUSE", "COMPUTE_WH"),
        database=os.environ.get("SF_DATABASE", "HACKATHON"),
        schema=os.environ.get("SF_SCHEMA", "PUBLIC"),
    )

@app.route("/api/customers", methods=["GET", "OPTIONS"])
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER_ARR")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/hotels", methods=["GET", "OPTIONS"])
def get_hotels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HOTEL_ARR")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/claude", methods=["POST", "OPTIONS"])
def claude_proxy():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "Anthropic API key not configured"}), 500

    body = request.get_json()
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model=body.get("model", "claude-sonnet-4-20250514"),
        max_tokens=body.get("max_tokens", 1000),
        system=body.get("system", ""),
        messages=body.get("messages", [])
    )

    response = jsonify({
        "content": [{"type": "text", "text": message.content[0].text}]
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)