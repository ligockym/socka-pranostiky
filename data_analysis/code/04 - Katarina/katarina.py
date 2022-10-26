import statistics

import numpy
from Parser import Parser
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
from scipy.stats import pearsonr


# Station id only for label
def generate_graph(data):
    """
    Generate graph from data that are passed in parameter

    :param data: dict with keys from calculate_values() and 'station_id', 'station_lat'...
    :return: just beautiful graphs :)
    """

    # Create traces with graph (line)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['years'], y=data['success_failure'],
                             marker=dict(
                                 color=data['success_failure'],
                                 colorscale=[(0, "red"), (0.5, "blue"), (1, "green")],
                                 cmin=0,
                                 cmax=1,
                             ),
                             marker_color=data['success_failure'],
                             mode='markers',
                             name='Platila pranostika'))

    fig.update_yaxes(range=[-0.5,1.5])

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
            tickvals=[0, 0.5, 1],
            ticktext=['Neplatila', 'Neurčené', 'Platila'],
            title_standoff=25),
        font=dict(family='Barlow', size=14, color='#4A5672'),
        title={
            'text': "Katarína na blate, Vianoce na zlate <br>Číslo stanice: " + str(data['station_id']) + " Úspešnosť: " + str(data['success_rate']) + "%",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    parser_mean_temp.write_graph_to_file(fig, 'katarina', str(data['station_id']))


#
# station_data: dict in format {'date': datetime, 'value': temperature}, will contain values for first septembers only
# return:


def calculate_values(station_data_precipitation: dict, station_data_mean_temp: dict, station_data_snow_depth: dict):
    """
     Calculates data needed to generate graphs and files.
    :param station_data: data for each day; dict in format {'date': datetime, 'value': temperature}
    :return:
    """

    # will hold precipitation on Katarina, snow depth on Christmas Eve and years
    result = {'katarina_temp': [], 'katarina_precipitation': [], 'katarina_mug': [],
              'christmas_snow': [], 'christmas_was_snow': [], 'years': [], 'success_failure': [], 'success_rate': 0}

    # loop through all days,
    # take Katarina data and chrismas eve data
    for i in range(len(station_data_precipitation)):
        item_precipitation = station_data_precipitation[i]
        item_mean_temp = station_data_mean_temp[i]
        item_snow_depth = station_data_snow_depth[i]
        date = item_precipitation['date']

        # is katarina
        if date.month == 11 and date.day == 25:
            result['katarina_temp'] = float(item_mean_temp['value'])
            result['katarina_precipitation'] = float(item_precipitation['value'])
            if result['katarina_temp'] > 0 and result['katarina_precipitation'] > 0:
                # there was rain and not freezing = mug
                result['katarina_mug'].append(1)
            else:
                result['katarina_mug'].append(0)

        # is christmas eve
        if date.month == 12 and date.day == 24:
            snow = float(item_snow_depth['value'])
            if snow == 9999.0:
                result['christmas_was_snow'].append(-1)
            elif snow > 0:
                result['christmas_was_snow'].append(1)
            else:
                result['christmas_was_snow'].append(0)
            result['christmas_snow'].append(snow)

            result['years'].append(date.year)


    for i in range(len(result['years'])):
        if result['katarina_mug'][i] == 1:
            if result['christmas_was_snow'][i] == 1:
                result['success_failure'].append(1)
            elif result['christmas_was_snow'][i] == -1:
                # undefined snow (9999.9 value)
                result['success_failure'].append(0.5)
            else:
                result['success_failure'].append(0)
        else:
            # not defined because there was no mug on Katarina
            result['success_failure'].append(0.5)

    number_of_success = len([x for x in result['success_failure'] if x == 1])
    number_of_failure = len([x for x in result['success_failure'] if x == 0])
    number_of_none = len([x for x in result['success_failure'] if x == 0.5])
    number_of_all = number_of_success + number_of_failure + number_of_none
    if number_of_all != number_of_none:
        result['success_rate'] = round((number_of_success / (number_of_all - number_of_none) * 100), 2)
    else:
        result['success_rate'] = 0

    # calculate correlation between two datasets
    return result


parser_mean_temp = Parser('..\Data\Mean temperature\CARPATGRID_TA_D.ser')
parser_precipitation = Parser('..\Data\Precipitation\CARPATGRID_PREC_D.ser')
parser_snow_depth = Parser('..\Data\Snow\CARPATGRID_SNOW_D.ser')

chart_studio.tools.set_credentials_file(username='ligockym', api_key='DR4Sf7O1pcMzvpBF3e2N')
chart_studio.tools.set_config_file(world_readable=True,
                                   sharing='public')
max_number_stations = 5895
group_stations = list(range(1, max_number_stations + 1))
group_stations = numpy.array_split(group_stations, (max_number_stations // 70) + 1)


for i in range(len(group_stations)):

    data_mean_temp = parser_mean_temp.load_data(group_stations[i])
    data_precipitation = parser_precipitation.load_data(group_stations[i])
    data_snow_depth = parser_snow_depth.load_data(group_stations[i])

    for station_id in data_mean_temp.keys():
        station_data_mean_temp = data_mean_temp[station_id]
        station_data_precipitation = data_precipitation[station_id]
        station_data_snow_depth = data_snow_depth[station_id]
        calculated_values = calculate_values(station_data_precipitation, station_data_mean_temp, station_data_snow_depth)
        # merge calculated values with info about station
        calculated_values = {**parser_mean_temp.get_info_for_station(station_id), **calculated_values}

        generate_graph(calculated_values)
        parser_mean_temp.write_info_to_file(calculated_values, 'csv/katarina.csv')
        print("Graph generated for station " + str(station_id))
