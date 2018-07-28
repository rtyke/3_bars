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
        print('В файле данные не формате json')
        return None


def get_biggest_bar(data):
    biggest_bar = max(
        data,
        key=lambda x: x['properties']['Attributes']['SeatsCount'])
    biggest_bar_name = biggest_bar['properties']['Attributes']['Name']
    biggest_bar_seats = biggest_bar['properties']['Attributes']['SeatsCount']
    return biggest_bar_name, biggest_bar_seats


def get_smallest_bar(data):
    smallest_bar = min(
        data,
        key=lambda x: x['properties']['Attributes']['SeatsCount'])
    smallest_bar_name = smallest_bar['properties']['Attributes']['Name']
    smallest_bar_seats = smallest_bar['properties']['Attributes']['SeatsCount']
    return smallest_bar_name, smallest_bar_seats


def get_closest_bar(data, longitude, latitude):
    # TODO map or lambda?
    func = lambda x: ((x['geometry']['coordinates'][0] - longitude) ** 2 +
                      (x['geometry']['coordinates'][1] - latitude) ** 2)**1/2
    closest_bar = min(data, key=func)
    closest_bar_name = closest_bar['properties']['Attributes']['Name']
    closest_bar_address = closest_bar['properties']['Attributes']['Address']
    return closest_bar_name, closest_bar_address


def get_json_path():
    try:
        json_path = sys.argv[1]
    except IndexError:
        json_path = input('Введите полный путь к файлу с json данным:\n')
    return json_path


def is_geo_coordinates(user_input):
    if len(user_input) == 9 and user_input[2] == '.' :
        try:
            float(user_input)
        except ValueError:
            return False
        else:
            return True


def get_user_location():
    while True:
        longitude = input('Введите долготу места, рядом с котором ищем бар:\n')
        if not is_geo_coordinates(longitude):
            print('Долгота введена неверно, попробуйте еще раз\n')
        else:
            break
    while True:
        latitude = input('Введите широту места, рядом с которым ищем бар:\n')
        if not is_geo_coordinates(latitude):
            print('Широта введена неверно, попробуйте еще раз\n')
        else:
            break
    return float(longitude), float(latitude)


if __name__ == '__main__':
    json_path = get_json_path()
    bars_attr = load_data(json_path)
    if not bars_attr:
        sys.exit('Скрипт не может рабоать без данных')
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
    print(f'Самый близкий бар: {closest_bar[0]}, aдрес: {closest_bar[1]} ')




