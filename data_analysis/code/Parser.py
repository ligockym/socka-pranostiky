import datetime
import os
import csv

class Parser:

    def __init__(self, file_path):
        self.file_path = '../../../Data/' + file_path
        self.coordinates = {}
        self.load_coordinates()

    def load_data(self, stations):
        print("Start with parsing file:")
        self.data = {}
        for station in stations:
            self.data[station] = []

        with open(self.file_path, 'r') as file:
            i = 0
            for line_raw in file:
                if (i == 0):
                    i += 1
                    continue
                else:
                    line = line_raw.split()
                    for station in stations:
                        # plus two because first three rows are year, month, day
                        value = line[station + 2]
                        dt = datetime.datetime(year=int(line[0]), month=int(line[1]), day=int(line[2]))
                        self.data[station].append({'date': dt, 'value': value})
                    i += 1
        print("End of parsing of file")
        return self.data

    def get_data(self):
        return self.data

    def write_graph_to_file(self, fig, folder, name):
        path = '../../results/images/' + folder
        if not os.path.exists(path):
            os.mkdir(path)

        fig.write_image(path + '/' + name + '.svg', format='svg')


    def load_coordinates(self):
        self.coordinates = {}
        with open('../../../Data/Mean temperature/PredtandfilaGrid.dat') as file:
            i = 0
            for line_raw in file:
                # continue in case of first line
                if (i == 0):
                    i += 1
                    continue
                else:
                    line = line_raw.split()
                    self.coordinates[int(line[0])] = {'lon': line[1], 'lan': line[2], 'country': line[3],
                                                 'altitude': line[4]}

    def get_info_for_station(self, station_id):
        """
        Returns dict with lat, lot, country, altitude for a specific station_id

        :param station_id:
        :return: dict with lat, lot, country, altitude
        """
        result = {}
        result['station_id'] = station_id
        # prefix all values with station_
        for key, value in self.coordinates[station_id].items():
            result['station_' + key] = value
        return result


    def write_info_to_file(self, data: dict, file_name):
        """
        Responsible for writing info about calculations into a csv file

        :param data: dict with keys such as correlation, first_sept_diff; station key has to exist with
        :return:
        """

        if 'station_id' not in data:
            print("You need to add station_id, station_lon, station_lan, station_country to data parameter")
            return False

        fieldnames = data.keys()
        last_found_id = 0
        path_to_file = '../../results/' + file_name
        if os.path.exists(path_to_file):
            with open(path_to_file, 'r+', newline='') as file:
                reader = csv.DictReader(file, fieldnames=fieldnames)
                i = 0
                for row in reader:
                    i = i+1
                    if i == 1:
                        # because it is header
                        continue
                    last_found_id = int(row['station_id'])

        with open(path_to_file, 'a+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if last_found_id == 0:
                writer.writeheader()
            # prevent having duplicate lines in csv file
            should_write = True
            for key, value in list(data.items()):
                # if station id of data item is less than last found id
                if key == 'station_id' and value <= last_found_id:
                    should_write = False
                    break
            if (should_write):
                writer.writerow(data)
            else:
                print("Warning: skipped item with station_id", data['station_id'], "because this item is already in csv file.")

