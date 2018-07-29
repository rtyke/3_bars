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


def get_seats_count(bar_dict):
    return bar_dict['properties']['Attributes']['SeatsCount']


def get_bar_name(bar_dict):
    return bar_dict['properties']['Attributes']['Name']


def get_bar_address(bar_dict):
    return bar_dict['properties']['Attributes']['Address']


def get_biggest_bar(bar_dict):
    biggest_bar_dict = max(bar_dict, key=get_seats_count)
    return get_bar_name(biggest_bar_dict), get_seats_count(biggest_bar_dict)


def get_smallest_bar(bar_dict):
    smallest_bar_dict = min(bar_dict, key=get_seats_count)
    return get_bar_name(smallest_bar_dict), get_seats_count(smallest_bar_dict)


def get_closest_bar(bar_dict, latitude, longitude):

    def calculate_distance(data_dict):
        bar_long, bar_lat = data_dict['geometry']['coordinates']
        return ((bar_long - longitude)**2 + (bar_lat - latitude)**2)*0.5

    closest_bar_dict = min(bar_dict, key=calculate_distance)
    return get_bar_name(closest_bar_dict), get_bar_address(closest_bar_dict)


def get_path():
    try:
        path = sys.argv[1]
    except IndexError:
        path = input('Введите полный путь к файлу с json данным:\n')
    return path


def get_users_longitude():
    longitude = input('Введите долготу места, рядом с которой ищем бар:\n')
    try:
        longitude = float(longitude)
        return longitude
    except ValueError:
        print('Долгота введена неверно, попробуйте еще раз\n')
        return get_users_longitude()


def get_users_latitude():
    latitude = input('Введите широту места, рядом с которой ищем бар:\n')
    try:
        latitude = float(latitude)
        return latitude
    except ValueError:
        print('Широта введена неверно, попробуйте еще раз\n')
        return get_users_latitude()


if __name__ == '__main__':
    json_path = get_path()
    bars_attr = load_data(json_path)
    if not bars_attr:
        sys.exit('Вы ввели неверный путь к файлу'.format(json_path))
    bars_json = convert_to_json(bars_attr)
    if not bars_json:
        sys.exit('Данные в файле не в формате json')
    bars_attr = bars_json['features']

    biggest_bar = get_biggest_bar(bars_attr)
    print('Самый большой бар: {}, мест:  {}'.format(
        biggest_bar[0], biggest_bar[1]))
    smallest_bar = get_smallest_bar(bars_attr)
    print('Самый маленький бар: {}, мест: {}'.format(
        smallest_bar[0], smallest_bar[1]))
    user_longitude = get_users_longitude()
    user_latitude = get_users_latitude()
    closest_bar = get_closest_bar(bars_attr, user_longitude, user_latitude)
    print('Самый близкий бар: {}, адрес: {}'.format(
        closest_bar[0], closest_bar[1]))
