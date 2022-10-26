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
    fig.add_trace(go.Scatter(x=data['years'], y=data['first_snow_from_start'],
                             mode='lines',
                             name='Dátum prvého snehu'))
    y_starts_from = 100
    y_ends_to = 250
    step = 10
    # Y axis will be composed of dates (22.11, 3.2...) from 100th day from 1st June up to 250th day from 1st June
    tickvals = [x for x in range(y_starts_from, y_ends_to, step)]
    first_june = datetime.datetime.strptime("1.6.1999", '%d.%m.%Y')
    ticktext = []
    for value in tickvals:
        value_date = first_june + datetime.timedelta(days=value)
        ticktext.append(str(value_date.day) + "." + str(value_date.month))

    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext
        )
    )

    fig.update_yaxes(range=[y_starts_from, y_ends_to])

    fig.add_trace(go.Scatter(x=data['years'], y=data['linear_regression'],
                             mode='lines',
                             name='Trend'))

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
                x=-0.15,
                y=0.5,
                showarrow=False,
                text="Dátum prvého snehu",
                textangle=-90,
                xref="paper",
                yref="paper"
            )
        ],
        font=dict(family='Barlow', size=14, color='#4A5672'),
        title={
            'text': "Dátum prvého snehu <br>Číslo stanice: " + str(
                data['station_id']),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    parser.write_graph_to_file(fig, 'first-snow', str(data['station_id']))


#
# station_data: dict in format {'date': datetime, 'value': temperature}, will contain values for first septembers only
# return:


def calculate_values(station_data: dict):
    """
     Calculates data needed to generate graphs and files.
    :param station_data: data for each day; dict in format {'date': datetime, 'value': temperature}
    :return:
    """

    result = {'first_snow_date': [], 'first_snow_from_start': [], 'years': [], 'average_first_snow_date': None,
              'average_first_snow_from_start': None}

    # loop through all days,
    # year is in different time (1961 is from 1.6.1961 to 31.5.1962)

    # reset to False always on 1.6
    snow_days_in_row = 0
    snow_found = None
    this_year = None
    for item in station_data:
        value = float(item['value'])

        # first half of first year is discarded because year starts from june
        if item['date'].year == 1961 and item['date'].month < 6:
            continue

        if not this_year:
            this_year = item['date'].year

        # if no snow
        if value == 0 or value == 9999.00:
            # reset snow found
            snow_days_in_row = 0
        else:
            snow_days_in_row += 1

        # this is the first time in this year with snow (note: 9999.00 is unspecified)
        if snow_days_in_row > 1 and not snow_found:
            start_of_this_year = datetime.datetime.strptime("1.6." + str(this_year), '%d.%m.%Y')
            from_start = item['date'] - start_of_this_year
            result['first_snow_date'].append(str(item['date'].day) + '.' + str(item['date'].month))
            result['first_snow_from_start'].append(from_start.days)
            result['years'].append(this_year)
            snow_found = True

        # on last May reset year
        if item['date'].month == 5 and item['date'].day == 31:
            snow_found = False
            snow_days_in_row = 0
            this_year = item['date'].year

    # calculate LinearRegression
    x = numpy.array(result['years']).reshape((-1, 1))
    y = numpy.array(result['first_snow_from_start'])

    # transform data by some special magic
    # create model
    model = LinearRegression().fit(x, y)

    # find y coords of linear regression line
    result['linear_regression'] = model.predict(x)
    result['intercept'] = model.intercept_

    # calculate average first snow date and average first snow from start
    result['average_first_snow_from_start'] = int(statistics.mean(result['first_snow_from_start']))
    first_june = datetime.datetime.strptime("1.6.1999", '%d.%m.%Y')
    result['average_first_snow_date'] = first_june + datetime.timedelta(days=result['average_first_snow_from_start'])
    result['average_first_snow_date'] = str(result['average_first_snow_date'].day) + '.' +  str(result['average_first_snow_date'].month)

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
        parser.write_info_to_file(calculated_values, 'csv/first_snow.csv')
        print("Graph generated")
