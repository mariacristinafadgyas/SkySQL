import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from data import FlightDataVisuals


def plot_percentage_of_delayed_flights_by_airline(data):
    """
    Plots the percentage of delayed flights by airline.
    """
    if not data:
        print("No data available to plot.")
        return

    # Extract data for plotting
    airlines = [record[0] for record in data]
    percentages = [record[3] for record in data]

    plt.figure(figsize=(8, 5))
    plt.bar(airlines, percentages, color='tab:olive')
    plt.xlabel('Airline')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title('Percentage of Delayed Flights by Airline')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('delayed_flights_per_airline.png')
    plt.show()


def plot_percentage_of_delayed_flights_per_hour(data):
    """
    Plots the percentage of delayed flights per hour of the day.
    """
    # Extract columns from the tuple based on the expected order
    hours = [record[0] for record in data]  # Extract 'hour_of_day'
    percentages = [record[3] for record in data]  # Extract 'delayed_percentage'

    # Convert hours to integers for the x-axis
    hours = list(map(int, hours))

    # Normalize the percentage data for the color gradient
    norm = plt.Normalize(min(percentages), max(percentages))
    colors = cm.viridis_r(norm(percentages))  # Using the 'viridis' colormap for the gradient

    plt.figure(figsize=(12, 7))
    bars = plt.bar(hours, percentages, color=colors, edgecolor='black')

    # Add color gradient bar (legend)
    sm = plt.cm.ScalarMappable(cmap="viridis_r", norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, orientation='vertical', pad=0.02)
    cbar.set_label('Percentage of Delayed Flights')

    plt.xlabel('Hour of Day')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title('Percentage of Delayed Flights per Hour of the Day')
    plt.xticks(np.arange(0, 24, step=1))  # Set x-ticks for every hour
    plt.tight_layout()
    plt.savefig('percentage_of_delayed_flights_per_hour.png')
    plt.show()


def plot_heatmap_of_delayed_flights_by_route(data):
    """
    Plots the heatmap of the delayed flights by route.
    """
    routes = [(record[0], record[1], record[4]) for record in
              data]  # Extract 'origin', 'destination', 'delayed_percentage'
    origins = list(set(record[0] for record in routes))
    destinations = list(set(record[1] for record in routes))

    # Create a 2D array to hold the delayed percentages
    heatmap_data = np.zeros((len(origins), len(destinations)))

    # Fill the heatmap data
    origin_to_index = {origin: idx for idx, origin in enumerate(origins)}
    destination_to_index = {destination: idx for idx, destination in enumerate(destinations)}

    for origin, destination, percentage in routes:
        heatmap_data[origin_to_index[origin], destination_to_index[destination]] = percentage

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, xticklabels=destinations, yticklabels=origins, cmap='PiYG', annot=False, fmt=".1f")
    plt.xlabel('Destination Airport')
    plt.ylabel('Origin Airport')
    plt.title('Percentage of Delayed Flights by Route')
    plt.tight_layout()
    plt.savefig('percentage_of_delayed_flights_by_route.png')
    plt.show()


def plot_routes_on_map(data):
    """
    Plot the percentage of delayed flights per route on a map of the USA.
    """
    plt.figure(figsize=(12, 8))

    # Setup Basemap for USA
    m = Basemap(projection='lcc', resolution='c',
                lat_0=37.5, lon_0=-95,
                width=5E6, height=3E6)

    m.shadedrelief()
    m.drawcoastlines(color='gray')
    m.drawcountries(color='gray')
    m.drawstates(color='gray')

    # Create a color map for the delays
    max_delay = max(record[4] for record in data)
    min_delay = min(record[4] for record in data)
    norm = plt.Normalize(vmin=min_delay, vmax=max_delay)
    cmap = plt.get_cmap('Spectral')

    # Plot each route
    for record in data:
        origin = record[0]
        destination = record[1]
        percentage = record[4]
        origin_latitude = record[5]
        origin_longitude = record[6]
        destination_latitude = record[7]
        destination_longitude = record[8]

        x_o, y_o = m(origin_longitude, origin_latitude)
        x_d, y_d = m(destination_longitude, destination_latitude)

        color = cmap(norm(percentage))
        m.plot([x_o, x_d], [y_o, y_d], marker=None, color=color, linewidth=2)

    # Add color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, orientation='horizontal', pad=0.05, label='Percentage of Delayed Flights')

    # Add a title
    plt.title('Percentage of Delayed Flights per Route', fontsize=15)
    plt.tight_layout()
    plt.savefig('delayed_flights_routes_map.png')
    plt.show()


def main():
    db_uri = 'sqlite:///data/flights.sqlite3'
    flight_data_visuals = FlightDataVisuals(db_uri)
    data = flight_data_visuals.get_percentage_of_delayed_flights_by_airline()
    plot_percentage_of_delayed_flights_by_airline(data)
    data = flight_data_visuals.get_percentage_of_delayed_flights_per_hour()
    plot_percentage_of_delayed_flights_per_hour(data)
    data = flight_data_visuals.get_delayed_flights_per_route()
    plot_heatmap_of_delayed_flights_by_route(data)
    data = flight_data_visuals.get_delayed_flights_per_route_with_coordinates()
    plot_routes_on_map(data)


if __name__ == "__main__":
    main()
