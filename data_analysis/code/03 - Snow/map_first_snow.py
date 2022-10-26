import datetime

from map import Map
from statistics import mean


class FirstSnowMap(Map):
    '''
    creates map graph with averaged first snow values
    '''

    def __init__(self, source_file_path, graph_name):
        super(FirstSnowMap, self).__init__(source_file_path, graph_name)

    def _prepareYAxisLabels(self):
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
        return (tickvals, ticktext)

    def run(self):
        tickvals, ticktext = self._prepareYAxisLabels()

        graph_options = dict(
            z=[x['average_first_snow_from_start'] for x in self._map_data],
            zmin=120, zmax=200,
            customdata=[
                self.convert_customdata(x, ['station_country_name', 'average_first_snow_date', 'station_altitude',
                                            'station_id',
                                            'station_lan', 'station_lon']) for x in self._map_data],
            hovertemplate=
            "<i>Prvý sneh</i>: %{customdata.average_first_snow_date}" +
            "<br><i>Krajina</i>: %{customdata.station_country_name}<br>" +
            "<i>Výška</i>: %{customdata.station_altitude}m.n.m <br>" +
            "<i>Stanica</i>: %{customdata.station_id} <br>" +
            "<i>Zem. šírka</i>: %{customdata.station_lan} <br>" +
            "<i>Zem. výška</i>: %{customdata.station_lon} <br>" +
            "",
            colorbar=dict(
                tickmode='array',
                tickvals=tickvals,
                ticktext=ticktext
            )
        )
        self.generate_map_graph(graph_options)


first_snow_map = FirstSnowMap('csv/first_snow.csv', 'first-snow')
first_snow_map.run()
