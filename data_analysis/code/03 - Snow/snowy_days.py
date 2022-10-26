import datetime
import statistics

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
def generate_graph(data):
    """
    Generate graph from data that are passed in parameter

    :param data: dict with keys from calculate_values() and 'station_id', 'station_lat'...
    :return: just beautiful graphs :)
    """

    # Create traces with graph (line)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['years'], y=data['was_snow'],
                             marker=dict(
                                 size=10,
                                 color=data['snow_values'],
                                 cmin=0,
                                 cmax=15,
                                 colorscale="Viridis",
                                 colorbar=dict(
                                     title="Sneh (cm)"
                                 ),
                             ),
                             mode='markers',
                             name='Sneh (1: bol, 0: nebol)',
                             showlegend=False)
                  )

    fig.add_trace(go.Scatter(x=data['years'], y=data['linear_regression'],
                             mode='lines',
                             showlegend=False))
    fig.update_yaxes(range=[0, 365])

    # add labels for
    fig.update_layout(
        yaxis=dict(
            title_text="Počet dní so snehom"),
        font=dict(family='Barlow', size=14, color='#4A5672'),
        title={
            'text': "Dni so snehom <br>Číslo stanice: " + str(
                data['station_id']),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    # py.plot(fig, filename='vianoce-sneh')

    parser.write_graph_to_file(fig, 'snowy-days', str(data['station_id']))


#
# station_data: dict in format {'date': datetime, 'value': temperature}, will contain values for first septembers only
# return:


def calculate_values(station_data: dict):
    """
     Calculates data needed to generate graphs and files.
    :param station_data: data for each day; dict in format {'date': datetime, 'value': temperature}
    :return:
    """

    result = {'percentage': None, 'years': [], 'was_snow': [], 'snow_values': []}
    this_year = station_data[0]['date'].year  # first year
    num_of_days_year = 0
    # number of days with snow for year
    was_snow = 0

    # values of snow (mean)
    snow_values = []
    # loop through all days
    for item in station_data:
        value = float(item['value'])
        num_of_days_year += 1

        if value == 0 or value == 9999.00:  # no snow
            pass
        else:
            was_snow += 1
            snow_values.append(value)

        if this_year != item['date'].year:  # run on last day of a year
            result['was_snow'].append(was_snow)
            if len(snow_values) == 0:
                snow_values.append(0)
            result['snow_values'].append(round(statistics.mean(snow_values), 2))
            result['years'].append(item['date'].year)
            was_snow = 0
            snow_values = []
            this_year = item['date'].year
            num_of_days_year = 0

    # get number of snowy days for whole period
    result['percentage'] = round((len([x for x in result['was_snow'] if x > 0]) / len(result['years'])) * 100, 2)

    # calculate LinearRegression
    x = numpy.array(result['years']).reshape((-1, 1))
    y = numpy.array(result['was_snow'])

    # transform data by some special magic
    # create model
    model = LinearRegression().fit(x, y)

    # find y coords of linear regression line
    result['linear_regression'] = model.predict(x)
    result['intercept'] = model.intercept_
    # dict with result data
    return result


parser = Parser('..\Data\Snow\CARPATGRID_SNOW_D.ser')

chart_studio.tools.set_credentials_file(username='ligockym', api_key='DR4Sf7O1pcMzvpBF3e2N')
chart_studio.tools.set_config_file(world_readable=True,
                                   sharing='public')
max_number_stations = 5895
group_stations = list(range(1, max_number_stations + 1))
group_stations = numpy.array_split(group_stations, (max_number_stations // 50) + 1)

for i in range(len(group_stations)):
    data = parser.load_data(group_stations[i])

    for station_id, station_data in data.items():
        calculated_values = calculate_values(station_data)
        # merge calculated values with info about station
        calculated_values = {**parser.get_info_for_station(station_id), **calculated_values}

        generate_graph(calculated_values)
        parser.write_info_to_file(calculated_values, 'csv/snowy-days.csv')
        print("Graph generated")
