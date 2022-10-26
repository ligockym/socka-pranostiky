import statistics

import numpy
from Parser import Parser
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
from scipy.stats import pearsonr


# Station id only for label
def generate_graph(data, month_number, month_slug, month_name):
    """
    Generate graph from data that are passed in parameter

    :param data: dict with keys from calculate_values() and 'station_id', 'station_lat'...
    :return: just beautiful graphs :)
    """

    # Create traces with graph (line)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['years'], y=data['first_sept_differences'],
                             mode='lines',
                             name='1.' + month_name.lower()))

    fig.add_trace(go.Scatter(x=data['years'], y=data['sept_differences'],
                             mode='lines',
                             name='Celý ' + month_name.lower()))

    fig.update_yaxes(range=[-10, 10])

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
                text="Odchýlka od normálu [°C]",
                textangle=-90,
                xref="paper",
                yref="paper"
            )
        ],
        font=dict(family='Barlow', size=14, color='#4A5672'),
        title={
            'text': "Odchýlka od normálu pre prvý deň v mesiaci a pre celý mesiac " + month_name.lower() + "<br>Číslo stanice: " + str(data['station_id']),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    parser.write_graph_to_file(fig, 'first-' + month_slug, str(data['station_id']))


#
# station_data: dict in format {'date': datetime, 'value': temperature}, will contain values for first septembers only
# return:


def calculate_values(station_data: dict, month_number, month_slug, month_name):
    """
     Calculates data needed to generate graphs and files.
    :param station_data: data for each day; dict in format {'date': datetime, 'value': temperature}
    :return:
    """

    # will hold differences from normal temp of first september and september; and other data
    result = {'first_sept_differences': [], 'sept_differences': [], 'number_of_same_match': 0,
              'number_of_diff_match': 0, 'years': []}

    # dict in format {year: temperature for first september}
    first_sept_values = {}
    # dict in format {year: [temperature for each day in september in the year]}
    september_values = {}

    # loop through all days,
    # take first september and september values out into first_sept_values and september_values
    for item in station_data:
        # is first of september?
        if item['date'].month == month_number and item['date'].day == 1:
            first_sept_values[item['date'].year] = float(item['value'])

        # is september?
        if item['date'].month == month_number:
            if not item['date'].year in september_values:
                # if array is not initialized, init it
                september_values[item['date'].year] = []
            september_values[item['date'].year].append(float(item['value']))

    # apply arithmetic mean to first september values
    normal_temp_first_sept = statistics.mean(first_sept_values.values())

    # loop through each year, calculate mean for september of the specific year
    # and then calculate normal temp for all times by using arithmetic mean for all septembers
    normal_temp_sept = statistics.mean([statistics.mean(values) for year, values in september_values.items()])

    # number of times when both aspects were either positive or negative
    number_of_same_match = 0
    number_of_diff_match = 0

    # calculate difference between normal and actual
    for year, item in first_sept_values.items():
        # mean temp for this year's september
        mean_for_september = statistics.mean(september_values[year])

        # difference between this year's first september temp and normal first september temp
        diff_first_sept = item - normal_temp_first_sept

        # difference between this year's september and normal september temp
        diff_sept = mean_for_september - normal_temp_sept

        # two positive = positive, two negative = positive :)
        if (diff_first_sept * diff_sept) > 0:
            number_of_same_match += 1
        else:
            number_of_diff_match += 1

        result['first_sept_differences'].append(round(diff_first_sept, 2))
        result['sept_differences'].append(round(diff_sept, 2))
        result['years'].append(year)

    # calculate correlation between two datasets
    result['correlation'] = round(pearsonr(result['first_sept_differences'], result['sept_differences'])[0], 3)
    result['number_of_same_match'] = number_of_same_match
    result['number_of_diff_match'] = number_of_diff_match
    # dict with result data
    return result


parser = Parser('..\Data\Mean temperature\CARPATGRID_TA_D.ser')

chart_studio.tools.set_credentials_file(username='ligockym', api_key='DR4Sf7O1pcMzvpBF3e2N')
chart_studio.tools.set_config_file(world_readable=True,
                                   sharing='public')
max_number_stations = 5895
group_stations = list(range(1, max_number_stations + 1))
group_stations = numpy.array_split(group_stations, (max_number_stations // 70) + 1)

months = {'month_number': list(range(1,13)),
          'month_slug': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
          'month_name': ['Január', 'Február', 'Marec', 'Apríl', 'Máj', 'Jún', 'Júl', 'August', 'September', 'Október', 'November', 'December']}

for i in range(len(group_stations)):
    data = parser.load_data(group_stations[i])

    for station_id, station_data in data.items():
        for i in range(12):
            calculated_values = calculate_values(station_data, months['month_number'][i], months['month_slug'][i], months['month_name'][i])
            # merge calculated values with info about station
            calculated_values = {**parser.get_info_for_station(station_id), **calculated_values}

            generate_graph(calculated_values, months['month_number'][i], months['month_slug'][i], months['month_name'][i])
            parser.write_info_to_file(calculated_values, 'csv/first_' + months['month_slug'][i] + '.csv')
            print("Graph generated for station " + str(station_id) + ', month ' + months['month_name'][i])
