import csv
import os
import inspect, os

import chart_studio
import plotly.graph_objects as go
import plotly.io as pio


class Map:

    def __init__(self, source_file_path, graph_name):
        chart_studio.tools.set_credentials_file(username='ligockym', api_key='DR4Sf7O1pcMzvpBF3e2N')
        chart_studio.tools.set_config_file(world_readable=True,
                                           sharing='public')
        self.__source_file_path = source_file_path
        self._map_data = self.parse_source_file()
        self._geojson = self.generate_geojson()
        self._graph_name = graph_name

    def get_country_info(self, country_id):
        '''
        Returns object with country_name and country_color

        :param country_id: from <1, 8>
        :return:
        '''
        countries = {
            1: {'country_name': 'Hungary', 'country_color': '#436F4D'},
            2: {'country_name': 'Serbia', 'country_color': '#C79D2D'},
            3: {'country_name': 'Romania', 'country_color': '#1A45E6'},
            4: {'country_name': 'Ukraine', 'country_color': '#2CA0E7'},
            5: {'country_name': 'Slovakia', 'country_color': '#144C9E'},
            6: {'country_name': 'Poland', 'country_color': '#DC173C'},
            7: {'country_name': 'Czechia', 'country_color': '#1D5089'},
            8: {'country_name': 'Croatia', 'country_color': '#905A60'},
        }
        return countries[country_id]

    def generate_geojson(self):
        '''
        Generates geojson for map data

        :param map_data:
        :return: geojson type of dict
        '''
        geojson = {
            'type': 'FeatureCollection',
            'features': []
        }

        for i in range(len(self._map_data)):
            geojson['features'].append(
                {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': []
                    },
                    'id': self._map_data[i]['station_id']
                })

            coords = self.generate_coords_from_point(self._map_data[i]['station_lon'], self._map_data[i]['station_lan'])
            geojson['features'][i]['geometry']['coordinates'].append(coords)
        return geojson

    def parse_source_file(self):
        '''
        Takes source file from
        :param file_path:
        :return:
        '''
        map_data = []
        i = 0
        with open('../../results/' + self.__source_file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = self.parse_source_row(row)
                map_data.append(row)
                i += 1
        return map_data

    def parse_source_row(self, row):
        row['station_lon'] = float(row['station_lon'])
        row['station_lan'] = float(row['station_lan'])
        country_info = self.get_country_info(int(row['station_country']))
        row['station_country_name'] = country_info['country_name']
        row['station_country_color'] = country_info['country_color']
        return row

    def generate_map_graph(self, graph_options, layout_options={}):
        fig = go.Figure(go.Choroplethmapbox(geojson=self._geojson,
                                            locations=[x['station_id'] for x in self._map_data],
                                            marker_opacity=0.75, marker_line_width=0, **graph_options))

        fig.update_layout(
            mapbox={
                'style': "stamen-terrain",
                'center': {'lon': 22, 'lat': 47.4},
                'zoom': 4.8},
            showlegend=False)

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, **layout_options)


        fig.show()
        #py.plot(fig, filename=self._graph_name)
        path = '../../results/html/map_html'
        if not os.path.exists(path):
            os.mkdir(path)

        # DOWNLOAD does not work
        # fig.write_image(path + '/final_graph_' + graph_name.lower() + '.svg', format='svg')
        pio.write_html(fig, file=path + '/' + self._graph_name + '.html', auto_open=False, include_plotlyjs=False)


    def generate_coords_from_point(self, lat, lon, distance_between_points=0.1):
        '''
        Generates list of 5 coordinates with center point in lat and lon from parameter

        :param lat: latitude in form of float
        :param lon: longitude in form of float
        :param distance_between_points: distance between two center points
        :return:
        '''
        result = []
        half = distance_between_points / 2
        result.append([round(lat - half, 2), round(lon + half, 2)])
        result.append([round(lat + half, 2), round(lon + half, 2)])
        result.append([round(lat + half, 2), round(lon - half, 2)])
        result.append([round(lat - half, 2), round(lon - half, 2)])

        result.append([round(lat - half, 2), round(lon + half, 2)])

        return (result)

    def convert_customdata(self, object, indexes):
        '''
        Returns dict object with specified indexes

        :param object:
        :param indexes:
        :return:
        '''
        result = {}
        for index in indexes:
            result[index] = object[index]
        return result