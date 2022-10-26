import chart_studio
import json

from map import Map


class KatarinaMap(Map):
    def __init__(self, source_file_path, graph_name):
        super(KatarinaMap, self).__init__(source_file_path, graph_name)

    def run(self):
        graph_options = dict(
            z=[x['success_rate'] for x in self._map_data],
            zmin=0, zmax=100,
            customdata=[
                self.convert_customdata(x, ['station_country_name', 'success_failure', 'station_altitude', 'station_id',
                                            'station_lan', 'station_lon', 'success_rate']) for x in self._map_data],
            hovertemplate=
            "<br><i>Krajina</i>: %{customdata.station_country_name}<br>" +
            "<i>Úspešnosť</i>: %{customdata.success_rate}%<br>" +
            "<i>Výška</i>: %{customdata.station_altitude}m.n.m <br>" +
            "<i>Stanica</i>: %{customdata.station_id} <br>" +
            "<i>Zem. šírka</i>: %{customdata.station_lan} <br>" +
            "<i>Zem. výška</i>: %{customdata.station_lon} <br>" +
            "",
        )
        self.generate_map_graph(graph_options)

    def parse_source_row(self, row):
        '''
        :param row:
        :return:
        '''
        # should it be row = super(...)
        super(KatarinaMap, self).parse_source_row(row)
        return row


katarina_map = KatarinaMap('../results/csv/katarina.csv', 'katarina')
try:
    katarina_map.run()
except chart_studio.exceptions.PlotlyRequestError:
    print("Too large file")
    pass
