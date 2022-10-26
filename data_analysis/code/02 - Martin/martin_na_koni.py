import datetime
import statistics
import multiprocessing
import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

import numpy
from Parser import Parser
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


# Station id only for label
def generate_graph(data, threshold):
    """
    Generate graph from data that are passed in parameter

    :param data: dict with keys from calculate_values() and 'station_id', 'station_lat'...
    :return: just beautiful graphs :)
    """

    # Create traces with graph (line)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['years'], y=data['results'],
                             marker=dict(
                                 color=data['results'],
                                 colorscale=[(0, "red"), (1, "green")],
                                 cmin=0,
                                 cmax=1,
                             ),
                             marker_color=data['results'],
                             mode='markers',
                             name='Platila pranostika'))

    # add labels for
    fig.update_layout(
        annotations=[
            go.layout.Annotation(
                x=0.5,
                y=-0.15,
                showarrow=False,
                text="Roky",
                xref="paper",
                yref="paper"
            ),
            go.layout.Annotation(
                x=-0.1,
                y=0.5,
                showarrow=False,
                text="",
                textangle=-90,
                xref="paper",
                yref="paper"
            )
        ],
        yaxis=dict(
            title_text="",
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['Nesnežilo', 'Snežilo'],
            title_standoff=25),
        font=dict(family='Barlow', size=14, color='#4A5672'),
        title={
            'text': "Martin na bielom koni (rozptyl: " + str(threshold) + "dní) <br>Číslo stanice: " + str(
                data['station_id']) + " Úspešnosť: " + str(round(float(data['percentage']), 0)) + "%",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    parser.write_graph_to_file(fig, 'martin-th' + str(threshold), str(data['station_id']))


#
# station_data: dict in format {'date': datetime, 'value': temperature}, will contain values for first septembers only
# return:


def calculate_values(station_data: dict, threshold):
    """
     Calculates data needed to generate graphs and files.
    :param threshold: number of days which are considered as Martin's day (int)
    :param station_data: data for each day; dict in format {'date': datetime, 'value': temperature}
    :return:
    """

    result = {'percentage': None, 'years': [], 'results': []}
    days = [11]
    this_year = station_data[0]['date'].year
    was_snow_this_year = False

    for i in range(threshold):
        days.append(11 + i)
        days.append(11 - i)

    # loop through all days and look for snow on 11th November (Martin)
    for item in station_data:
        value = float(item['value'])
        if item['date'].month == 11 and item['date'].day in days:
            if value == 0 or value == 9999.00:  # no snow
                pass
            else:
                was_snow_this_year = True
        if this_year != item['date'].year:
            result['years'].append(item['date'].year)
            if was_snow_this_year:
                result['results'].append(1)  # append 1 if some snow
            else:
                result['results'].append(0)
            this_year = item['date'].year
            was_snow_this_year = False

    result['percentage'] = round(statistics.mean(result['results']) * 100, 2)
    # dict with result data
    return result


parser = Parser('Snow/CARPATGRID_SNOW_D.ser')

chart_studio.tools.set_credentials_file(username='ligockym', api_key='DR4Sf7O1pcMzvpBF3e2N')
chart_studio.tools.set_config_file(world_readable=True,
                                   sharing='public')
max_number_stations = 5895
group_stations = list(range(1, max_number_stations + 1))
group_stations = numpy.array_split(group_stations, (max_number_stations // 50) + 1)

def run_for_threshold(data, threshold):
    for station_id, station_data in data.items():
        calculated_values = calculate_values(station_data, threshold)
        # merge calculated values with info about station
        calculated_values = {**parser.get_info_for_station(station_id), **calculated_values}

        generate_graph(calculated_values, threshold)
        parser.write_info_to_file(calculated_values, 'csv/martin/martin-th-' + str(threshold) + '.csv')
        print("Graph generated for threshold:", threshold)

if __name__ == '__main__':
    processes = []
    for i in range(len(group_stations)):
        data = parser.load_data(group_stations[i])
        for threshold in range(0, 10):
            processes.append(multiprocessing.Process(target=run_for_threshold, args=(data, threshold)))
            processes[-1].start()

        processes = [x.join() for x in processes]
        processes = []