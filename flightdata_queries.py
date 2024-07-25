
QUERY_FLIGHT_BY_ID = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ID = :id
"""

QUERY_FLIGHT_BY_DATE = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights JOIN airlines ON flights.airline = airlines.id 
WHERE YEAR = :year AND MONTH = :month AND DAY = :day
"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights JOIN airlines ON flights.airline = airlines.id 
WHERE airlines.AIRLINE = :airline
"""

QUERY_DELAYED_FLIGHTS_BY_AIRPORT = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ORIGIN_AIRPORT = :airport
"""

QUERY_PERCENTAGE_OF_DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT 
    airlines.AIRLINE,
    COUNT(flights.ID) AS total_flights,
    COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) AS delayed_flights,
    (COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) * 100.0 / COUNT(flights.ID)) AS delayed_percentage
FROM flights
JOIN airlines ON flights.airline = airlines.id
GROUP BY airlines.AIRLINE;"""

QUERY_PERCENTAGE_OF_DELAYED_FLIGHTS_PER_HOUR = """
SELECT 
    SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 2) AS hour_of_day,
    COUNT(flights.ID) AS total_flights,
    COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) AS delayed_flights,
    (COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) * 100.0 / COUNT(flights.ID)) AS delayed_percentage
FROM flights
GROUP BY hour_of_day
ORDER BY hour_of_day;
"""

QUERY_DELAYED_FLIGHTS_BY_ROUTE = """
SELECT 
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    COUNT(flights.ID) AS total_flights,
    COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) AS delayed_flights,
    (COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) * 100.0 / COUNT(flights.ID)) AS delayed_percentage
FROM flights
GROUP BY flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT
ORDER BY flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT;
"""


QUERY_DELAYED_FLIGHTS_BY_ROUTE_WITH_COORD = """
SELECT 
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    COUNT(flights.ID) AS total_flights,
    COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) AS delayed_flights,
    (COUNT(CASE WHEN flights.DEPARTURE_DELAY > 0 THEN 1 END) * 100.0 / COUNT(flights.ID)) AS delayed_percentage,
    origin_airports.LATITUDE AS origin_latitude,
    origin_airports.LONGITUDE AS origin_longitude,
    dest_airports.LATITUDE AS destination_latitude,
    dest_airports.LONGITUDE AS destination_longitude
FROM flights
JOIN airports AS origin_airports ON flights.ORIGIN_AIRPORT = origin_airports.IATA_CODE
JOIN airports AS dest_airports ON flights.DESTINATION_AIRPORT = dest_airports.IATA_CODE
GROUP BY flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT
ORDER BY flights.ORIGIN_AIRPORT, flights.DESTINATION_AIRPORT;
"""