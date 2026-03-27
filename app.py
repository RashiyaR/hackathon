from flask import Flask, jsonify
from flask_cors import CORS
import snowflake.connector
import os

app = Flask(__name__)
CORS(app)  # Allows the dashboard to call this API from the browser

# ============================================================
# SNOWFLAKE CREDENTIALS — same as before
# ============================================================


def get_connection():
    return snowflake.connector.connect(
        account=os.environ.get("SF_ACCOUNT", "bljdbql-ueb08426"),
        user=os.environ.get("SF_USER", "rashiya"),
        password=os.environ.get("SF_PASSWORD", "Product1234567"),
        warehouse=os.environ.get("SF_WAREHOUSE", "COMPUTE_WH"),
        database=os.environ.get("SF_DATABASE", "HACKATHON"),
        schema=os.environ.get("SF_SCHEMA", "PUBLIC"),
    )
def get_connection():
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)


@app.route("/api/customers", methods=["GET"])
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER_ARR")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)


@app.route("/api/hotels", methods=["GET"])
def get_hotels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HOTEL_ARR")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
