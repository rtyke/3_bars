import json
import sys


def load_data(file_path):
    try:
        with open(file_path, 'r') as file_object:
            bars_data = file_object.read()
            return bars_data
    except FileNotFoundError:
        return None


def convert_to_json(string_data):
    try:
        json_data = json.loads(string_data)
        return json_data
    except json.decoder.JSONDecodeError:
        return None


def print_bar(bar_dict, output, *features_names):
    feature_values = [bar_dict['properties']['Attributes'][x] for x
                      in features_names]
    print(output.format(*feature_values))


def get_seats_count(bar_dict):
    return bar_dict['properties']['Attributes']['SeatsCount']


def get_biggest_bar(bars_list):
    biggest_bar_dict = max(bars_list, key=get_seats_count)
    return biggest_bar_dict


def get_smallest_bar(bar_dict):
    smallest_bar_dict = min(bar_dict, key=get_seats_count)
    return smallest_bar_dict


def get_closest_bar(bar_dict, latitude, longitude):

    def calculate_distance(data_dict):
        bar_long, bar_lat = data_dict['geometry']['coordinates']
        return ((bar_long - longitude)**2 + (bar_lat - latitude)**2)*0.5

    closest_bar_dict = min(bar_dict, key=calculate_distance)
    return closest_bar_dict


def get_path():
    try:
        path = sys.argv[1]
    except IndexError:
        path = None
    return path


def get_users_cooridante(request):
    coordinate = input(request)
    try:
        coordinate = float(coordinate)
        return coordinate
    except ValueError:
        return None


if __name__ == '__main__':
    file_path = get_path()
    if not file_path:
        sys.exit('При запуске скрипта надо указать путь к файлу с данными в '
                 'формате json')
    bars_attr = load_data(file_path)
    if not bars_attr:
        sys.exit('Вы ввели неверный путь к файлу'.format(file_path))
    bars_json = convert_to_json(bars_attr)
    if not bars_json:
        sys.exit('Данные в файле не в формате json')
    bars_attr = bars_json['features']

    users_longitude = get_users_cooridante('Введите долготу места, рядом с '
                                           'которой ищем бар:\n')
    if not users_longitude:
        sys.exit('Долгота введена неверно')
    users_latitude = get_users_cooridante('Введите широту места, рядом с '
                                          'которой ищем бар:\n')
    if not users_latitude:
        sys.exit('Широта введена неверно')

    # define bars
    smallest_bar = get_smallest_bar(bars_attr)
    biggest_bar = get_biggest_bar(bars_attr)
    closest_bar = get_closest_bar(bars_attr, users_longitude, users_latitude)
    # output
    print_bar(smallest_bar, 'Самый маленький бар: {}, мест: {}',
               'Name', 'SeatsCount')
    print_bar(biggest_bar, 'Самый большой бар: {}, мест: {}',
               'Name', 'SeatsCount')
    print_bar(closest_bar, 'Самый близкий бар: {}, адрес: {}',
               'Name', 'Address')
