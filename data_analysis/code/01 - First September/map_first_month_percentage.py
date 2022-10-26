import chart_studio
import json

from map import Map


class FirstMonthMapPercentage(Map):
    def __init__(self, source_file_path, graph_name):
        super(FirstMonthMapPercentage, self).__init__(source_file_path, graph_name)

    def run(self):
        graph_options = dict(
            z=[x['percentage'] for x in self._map_data],
            zmin=40, zmax=80,
            customdata=[
                self.convert_customdata(x, ['station_country_name', 'percentage', 'station_altitude', 'station_id',
                                            'station_lan', 'station_lon', 'correlation']) for x in self._map_data],
            hovertemplate=
            "<i>Úspešnosť</i>: %{customdata.percentage}%<br>" +
            "<i>Korelácia</i>: %{customdata.correlation:.2f}" +
            "<br><i>Krajina</i>: %{customdata.station_country_name}<br>" +
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
        super(FirstMonthMapPercentage, self).parse_source_row(row)
        row['correlation'] = float(row['correlation'])
        row['matches'] = row['number_of_same_match'] + "/" + row['number_of_diff_match']
        row['percentage'] = round((int(row['number_of_same_match']) / (
                int(row['number_of_diff_match']) + int(row['number_of_same_match'])) * 100), 2)
        return row


months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
          'december']

for month in months:
    september_map = FirstMonthMapPercentage('../results/csv/first_' + month + '.csv', 'first-' + month + '-percentage')
    try:
        september_map.run()
    except chart_studio.exceptions.PlotlyRequestError:
        print("Too large file")
        pass
