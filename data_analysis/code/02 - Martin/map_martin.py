import datetime

from map import Map
from statistics import mean


class MartinMap(Map):
    '''
    creates map graph
    '''

    def __init__(self, source_file_path, graph_name):
        super(MartinMap, self).__init__(source_file_path, graph_name)

    def run(self):
        graph_options = dict(
            z=[x['percentage'] for x in self._map_data],
            zmin=0, zmax=100,
            customdata=[
                self.convert_customdata(x, ['station_country_name', 'percentage', 'station_altitude', 'station_id',
                                            'station_lan', 'station_lon']) for x in self._map_data],
            hovertemplate=
            "<i>Úspešnosť</i>: %{customdata.percentage}%<br>" +
            "<i>Krajina</i>: %{customdata.station_country_name}<br>" +
            "<i>Výška</i>: %{customdata.station_altitude}m.n.m <br>" +
            "<i>Stanica</i>: %{customdata.station_id} <br>" +
            "<i>Zem. šírka</i>: %{customdata.station_lan} <br>" +
            "<i>Zem. výška</i>: %{customdata.station_lon} <br>" +
            "",
        )
        self.generate_map_graph(graph_options)

for i in range(0,10):
    martin_map = MartinMap('csv/martin/martin-th-' + str(i) + '.csv', 'martin-th-' + str(i))
    martin_map.run()