from flask import Flask, jsonify, request
from main import *


app = Flask(__name__)

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
data_manager = data.FlightDataVisuals(SQLITE_URI)


def flight_by_id(data_manager, flight_id):
    """
    Fetches flight details by ID from the data manager and returns them.
    """
    results = data_manager.get_flight_by_id(flight_id)

    flight_details = []
    for result in results:
        result_dict = dict(result._mapping)
        delay = int(result_dict.get('DELAY', 0))
        flight_details.append({
            'ID': result_dict.get('ID'),
            'ORIGIN_AIRPORT': result_dict.get('ORIGIN_AIRPORT'),
            'DESTINATION_AIRPORT': result_dict.get('DESTINATION_AIRPORT'),
            'AIRLINE': result_dict.get('AIRLINE'),
            'DELAY': delay
        })
    return flight_details


def flights_by_date(data_manager, day, month, year):
    """
    Fetches flights by date from the data manager and returns them as a list of dictionaries.
    """
    results = data_manager.get_flights_by_date(day, month, year)

    flight_details = []
    for result in results:
        result_dict = dict(result._mapping)

        delay_str = result_dict.get('DELAY', '')
        try:
            delay = int(delay_str) if delay_str else 0
        except ValueError:
            delay = 0

        flight_details.append({
            'ID': result_dict.get('ID'),
            'ORIGIN_AIRPORT': result_dict.get('ORIGIN_AIRPORT'),
            'DESTINATION_AIRPORT': result_dict.get('DESTINATION_AIRPORT'),
            'AIRLINE': result_dict.get('AIRLINE'),
            'DELAY': delay
        })

    return flight_details


def delayed_flights_by_airline(data_manager, airline_name):
    """
    Fetches delayed flights by airline from the data manager and returns them.
    """
    results = data_manager.get_delayed_flights_by_airline(airline_name)

    flight_details = []
    for result in results:
        result_dict = dict(result._mapping)
        delay_str = result_dict.get('DELAY', '')
        try:
            delay = int(delay_str) if delay_str else 0
        except ValueError:
            delay = 0

        flight_details.append({
                'ID': result_dict.get('ID'),
                'ORIGIN_AIRPORT': result_dict.get('ORIGIN_AIRPORT'),
                'DESTINATION_AIRPORT': result_dict.get('DESTINATION_AIRPORT'),
                'AIRLINE': result_dict.get('AIRLINE'),
                'DELAY': delay
            })
    return flight_details


def delayed_flights_by_airport(data_manager, airport_code):
    """
    Fetches delayed flights by airport code from the data manager and returns them.
    """
    results = data_manager.get_delayed_flights_by_airport(airport_code)

    flight_details = []
    for result in results:
        result_dict = dict(result._mapping)

        delay_str = result_dict.get('DELAY', '')
        try:
            delay = int(delay_str) if delay_str else 0
        except ValueError:
            delay = 0

        flight_details.append({
            'ID': result_dict.get('ID'),
            'ORIGIN_AIRPORT': result_dict.get('ORIGIN_AIRPORT'),
            'DESTINATION_AIRPORT': result_dict.get('DESTINATION_AIRPORT'),
            'AIRLINE': result_dict.get('AIRLINE'),
            'DELAY': delay
        })

    return flight_details


@app.route('/api/flight_number', methods=['GET'])
def get_flight_by_number():
    flight_no = request.args.get('flight_no')
    if not flight_no:
        return jsonify({'error': 'Please provide a flight ID'}), 400

    try:
        flight_no = int(flight_no)  # Convert to integer
        flight_details = flight_by_id(data_manager, flight_no)
        if not flight_details:
            return jsonify({'error': 'No flight found with this ID'}), 404
        return jsonify(flight_details), 200
    except ValueError:
        return jsonify({'error': 'Invalid flight ID format'}), 400


@app.route('/api/flights_by_date', methods=['GET'])
def get_flights_by_date():
    # Get date from request arguments
    date_str = request.args.get('date')

    if not date_str:
        return jsonify({'error': 'Please provide a date in DD/MM/YYYY format'}), 400

    try:
        date = datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        return jsonify({'error': 'Date format must be DD/MM/YYYY'}), 400

    results = flights_by_date(data_manager, date.day, date.month, date.year)
    if not results:
        return jsonify({'message': 'No flights found for this date'}), 404
    return jsonify(results), 200


@app.route('/api/delayed_flights_by_airline', methods=['GET'])
def get_delayed_flights_by_airline():
    airline_name = request.args.get('airline_name')
    if not airline_name:
        return jsonify({'error': 'Please provide an airline name'}), 400

    flight_details = delayed_flights_by_airline(data_manager, airline_name)
    if not flight_details:
        return jsonify({'error': 'No flights found for this airline'}), 404

    return jsonify(flight_details), 200


@app.route('/api/delayed_flights_by_airport', methods=['GET'])
def get_delayed_flights_by_airport():
    airport_code = request.args.get('airport_code')

    if not airport_code or not (airport_code.isalpha() and len(airport_code) == 3):
        return jsonify({'error': 'Please provide a valid 3-letter airport code'}), 400

    results = delayed_flights_by_airport(data_manager, airport_code)
    if not results:
        return jsonify({'message': 'No delayed flights found'}), 404
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
