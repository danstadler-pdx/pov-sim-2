import logging
import os

import pyroscope
from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import generate_flight, get_random_int

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logging.getLogger("werkzeug").setLevel(logging.INFO)

# Stage 2.2 — Pyroscope continuous profiling.
# Pushes profiles direct to Grafana Cloud Pyroscope (bypasses Alloy by design).
pyroscope.configure(
    application_name=os.environ.get("PYROSCOPE_APPLICATION_NAME", "flights"),
    server_address=os.environ["PYROSCOPE_SERVER_ADDRESS"],
    basic_auth_username=os.environ["PYROSCOPE_BASIC_AUTH_USER"],
    basic_auth_password=os.environ["PYROSCOPE_BASIC_AUTH_PASSWORD"],
    tags={
        "service.namespace": "pov-sim",
        "deployment.environment": "lab",
    },
)

app = Flask(__name__)
Swagger(app)
CORS(app)
app.logger.setLevel(logging.INFO)
app.logger.info("flights service starting up")

@app.route('/health', methods=['GET'])
def health():
    """Health endpoint
    ---
    responses:
      200:
        description: Returns healthy
    """
    return jsonify({"status": "healthy"}), 200

@app.route("/", methods=['GET'])
def home():
    """No-op home endpoint
    ---
    responses:
      200:
        description: Returns ok
    """
    return jsonify({"message": "ok"}), 200

@app.route("/flights/<airline>", methods=["GET"])
def get_flights(airline):
    """Get flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: airline
        in: path
        type: string
        enum: ["AA", "UA", "DL"]
        required: true
      - name: raise
        in: query
        type: str
        enum: ["500"]
        required: false
    responses:
      200:
        description: Returns a list of flights for the selected airline
    """
    status_code = request.args.get("raise")
    if status_code:
      raise Exception(f"Encountered {status_code} error") # pylint: disable=broad-exception-raised
    count = get_random_int(1, 5)
    flights = [generate_flight(airline) for _ in range(count)]
    return jsonify({"airline_code": airline, "count": count, "flights": flights}), 200

@app.route("/flight", methods=["POST"])
def book_flight():
    """Book flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: passenger_name
        in: query
        type: string
        enum: ["John Doe", "Jane Doe"]
        required: true
      - name: flight_num
        in: query
        type: string
        enum: ["101", "202", "303", "404", "505", "606"]
        required: true
      - name: raise
        in: query
        type: str
        enum: ["500"]
        required: false
    responses:
      200:
        description: Booked a flight for the selected passenger and flight_num
    """
    status_code = request.args.get("raise")
    if status_code:
      raise Exception(f"Encountered {status_code} error") # pylint: disable=broad-exception-raised
    passenger_name = request.args.get("passenger_name")
    flight_num = request.args.get("flight_num")
    booking_id = get_random_int(100, 999)
    return jsonify({"passenger_name": passenger_name, "flight_num": flight_num, "booking_id": booking_id}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
