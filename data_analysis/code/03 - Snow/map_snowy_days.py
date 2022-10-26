import datetime
import json
import statistics

from map import Map
from statistics import mean


class SnowyMap(Map):
    '''
    creates map graph
    '''

    def __init__(self, source_file_path, graph_name):
        super(SnowyMap, self).__init__(source_file_path, graph_name)

    def run(self):
        print([x['was_snow'] for x in self._map_data])

    def run(self):
        graph_options = dict(
            z=[int(x['average_snow_days']) for x in self._map_data],
            zmin=20, zmax=200,
            customdata=[
                self.convert_customdata(x, ['station_country_name', 'was_snow', 'station_altitude', 'station_id',
                                            'station_lan', 'station_lon']) for x in self._map_data],
            hovertemplate=
            "<br><i>Krajina</i>: %{customdata.station_country_name}<br>" +
            "<br><i>Krajina</i>: %{customdata.station_country_name}<br>" +
            "<i>Výška</i>: %{customdata.station_altitude}m.n.m <br>" +
            "<i>Stanica</i>: %{customdata.station_id} <br>" +
            "<i>Zem. šírka</i>: %{customdata.station_lan} <br>" +
            "<i>Zem. výška</i>: %{customdata.station_lon} <br>" +
            "",
        )
        self.generate_map_graph(graph_options)

    def parse_source_row(self, row):
        super(SnowyMap, self).parse_source_row(row)
        row['was_snow'] = json.loads(row['was_snow'])
        row['average_snow_days'] = statistics.mean(row['was_snow'])
        return row


first_snow_map = SnowyMap('csv/snowy-days.csv', 'snowy-days')
first_snow_map.run()
