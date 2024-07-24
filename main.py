import data
from datetime import datetime
import sqlalchemy

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.
    """
    airline_input = input("\u001b[38;5;99;1mEnter airline name: \u001b[0m")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data object method "get_delayed_flights_by_airport".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        airport_input = input("\u001b[38;5;99;1mEnter origin airport IATA code: \u001b[0m")
        # Valide input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("\u001b[38;5;99;1mEnter flight ID: \u001b[0m"))
        except Exception as e:
            print("Try again...")
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            date_input = input("\u001b[38;5;99;1mEnter date in DD/MM/YYYY format: \u001b[0m")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    """
    Get a list of flight results (List of dictionary-like objects from SQLAachemy).
    Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.
    """
    print(f"\u001b[38;5;20;1mGot\u001b[0m \u001b[38;5;204;1m{len(results)}"
          f" \u001b[38;5;20;1mresults.\u001b[0m")
    for result in results:
        # turn result into dictionary
        result = result._mapping

        # Check that all required columns are in place
        try:
            delay = int(result['DELAY']) if result['DELAY'] else 0  # If delay columns is NULL, set it to 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("\u001b[38;5;160;1mError showing results: \u001b[0m", e)
            return

        # Different prints for delayed and non-delayed flights
        if delay and delay > 0:
            print(f"\u001b[38;5;220;1m{result['ID']}\u001b[0m. "
                  f"\u001b[38;5;49;1m{origin} -> {dest}\u001b[0m by "
                  f"\u001b[38;5;97;1m{airline}\u001b[0m, "
                  f"\u001b[38;5;196;1mDelay: {delay} Minutes\u001b[0m")
        else:
            print(f"\u001b[38;5;22;1m{result['ID']}\u001b[0m. "
                  f"\u001b[38;5;49;1m{origin} -> {dest}\u001b[0m by"
                  f" \u001b[38;5;97;1m{airline}\u001b[0m")


def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("\u001b[38;5;20;1mMenu:\u001b[0m")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            pass
        print("\u001b[38;5;160;1mTry again...\u001b[0m")

"""
Function Dispatch Dictionary
"""
FUNCTIONS = { 1: (flight_by_id, "\u001b[38;5;214;1mShow flight by ID\u001b[0m"),
              2: (flights_by_date, "\u001b[38;5;214;1mShow flights by date\u001b[0m"),
              3: (delayed_flights_by_airline, "\u001b[38;5;214;1mDelayed flights by airline\u001b[0m"),
              4: (delayed_flights_by_airport, "\u001b[38;5;214;1mDelayed flights by origin airport\u001b[0m"),
              5: (quit, "\u001b[38;5;160;1mExit\u001b[0m")
             }


def main():
    # Create an instance of the Data Object using our SQLite URI
    data_manager = data.FlightData(SQLITE_URI)

    # The Main Menu loop
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()