# coding: utf-8
import json
import sys


def load_data(filepath):
    try:
        with open(filepath, 'r') as file_object:
            data = file_object.read()
            return data
    except FileNotFoundError:
        print(f'Вы ввели неверный путь к файлу: {filepath}')
        return None


def convert_to_json(string_data):
    try:
        json_data = json.loads(string_data)
        return json_data
    except json.decoder.JSONDecodeError:
        print('Данные в файле не в формате json')
        return None


def get_seats_count(data):
    return data['properties']['Attributes']['SeatsCount']


def get_bar_name(data):
    return data['properties']['Attributes']['Name']


def get_bar_seats(data):
    return data['properties']['Attributes']['SeatsCount']


def get_bar_address(data):
    return data['properties']['Attributes']['Address']


def get_biggest_bar(data):
    biggest_bar_dict = max(data, key=get_seats_count)
    return get_bar_name(biggest_bar_dict), get_bar_seats(biggest_bar_dict)


def get_smallest_bar(data):
    smallest_bar_dict = min(data, key=get_seats_count)
    return get_bar_name(smallest_bar_dict), get_bar_seats(smallest_bar_dict)


def get_closest_bar(data, longitude, latitude):

    def calculate_distance(data):
        bar_long, bar_lat = data['geometry']['coordinates']
        return ((bar_long - longitude)**2 + (bar_lat - latitude)**2)*0.5

    closest_bar_dict = min(data, key=calculate_distance)
    return get_bar_name(closest_bar_dict), get_bar_address(closest_bar_dict)


def get_json_path():
    try:
        json_path = sys.argv[1]
    except IndexError:
        json_path = input('Введите полный путь к файлу с json данным:\n')
    return json_path


def is_geo_coordinates(user_input):
    if len(user_input) == 9 and user_input[2] == '.':
        try:
            float(user_input)
        except ValueError:
            return False
        else:
            return True


def get_user_location():
    while True:
        longitude = input('Введите долготу места, рядом с которой ищем бар:\n')
        if not is_geo_coordinates(longitude):
            print('Долгота введена неверно, попробуйте еще раз\n')
        else:
            break
    while True:
        latitude = input('Введите широту места, рядом с которой ищем бар:\n')
        if not is_geo_coordinates(latitude):
            print('Широта введена неверно, попробуйте еще раз\n')
        else:
            break
    return float(longitude), float(latitude)


if __name__ == '__main__':
    json_path = get_json_path()
    bars_attr = load_data(json_path)
    if not bars_attr:
        sys.exit('Скрипт не может работать без данных')
    bars_json = convert_to_json(bars_attr)
    if not bars_json:
        sys.exit('Данные должны быть в формате json')
    bars_attr = bars_json['features']

    biggest_bar = get_biggest_bar(bars_attr)
    print(f'Самый большой бар: {biggest_bar[0]}, мест:  {biggest_bar[1]}')
    smallest_bar = get_smallest_bar(bars_attr)
    print(f'Самый маленький бар: {smallest_bar[0]}, мест: {smallest_bar[1]}')
    user_longitude, user_latitude = get_user_location()
    closest_bar = get_closest_bar(bars_attr, user_longitude, user_latitude)
    print(f'Самый близкий бар: {closest_bar[0]}, адрес: {closest_bar[1]} ')




