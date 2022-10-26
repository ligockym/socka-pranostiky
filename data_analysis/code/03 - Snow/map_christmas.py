import datetime
import json
import statistics

from map import Map
from statistics import mean


class ChristmasMap(Map):
    '''
    creates map graph
    '''

    def __init__(self, source_file_path, graph_name):
        super(ChristmasMap, self).__init__(source_file_path, graph_name)

    def parse_source_row(self, row):
        '''
        :param row:
        :return:
        '''
        # should it be row = super(...)
        super(ChristmasMap, self).parse_source_row(row)
        row['percentage_number_of_days'] = round(statistics.mean([int(x) for x in json.loads(row['was_snow'])]), 1)
        return row

    def run(self):
        graph_options = dict(
            z=[x['percentage'] for x in self._map_data],
            zmin=0, zmax=100,
            customdata=[
                self.convert_customdata(x, ['station_country_name', 'was_snow', 'station_altitude', 'station_id',
                                            'station_lan', 'station_lon', 'percentage', 'percentage_number_of_days']) for x in self._map_data],
            hovertemplate=
            "<i>Úspešnosť</i>: %{customdata.percentage}%<br>" +
            "<i>Dni so snehom</i>: %{customdata.percentage_number_of_days}<br>" +
            "<br><i>Krajina</i>: %{customdata.station_country_name}<br>" +
            "<i>Výška</i>: %{customdata.station_altitude}m.n.m <br>" +
            "<i>Stanica</i>: %{customdata.station_id} <br>" +
            "<i>Zem. šírka</i>: %{customdata.station_lan} <br>" +
            "<i>Zem. výška</i>: %{customdata.station_lon} <br>" +
            "",
        )
        self.generate_map_graph(graph_options)


first_snow_map = ChristmasMap('csv/christmas-snow.csv', 'christmas-snow')
first_snow_map.run()
