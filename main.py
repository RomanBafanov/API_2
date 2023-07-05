from typing import Any
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import requests


BODY = {}

URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def shows_clicks(link, headers) -> Any:
    try:
        clicks = count_clicks(headers, link)
    except requests.exceptions.HTTPError:
        return None
    else:
        return clicks


def count_clicks(headers, link) -> Any:
    url = f'{URL}/{link}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def cut_and_show(link, headers):
    BODY['long_url'] = link
    try:
        bitlink = shorten_link(headers, URL, BODY)
    except requests.exceptions.HTTPError:
        return None
    else:
        return bitlink


def shorten_link(headers, url, body) -> Any:
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    return response.json()['link']


def is_bitlink(url):
    parsed = urlparse(url)
    if parsed.scheme == '':
        return False
    else:
        return True


def main(headers) -> Any:
    user_input = input('Введите ссылку ')
    if is_bitlink(user_input):
        bitlink = cut_and_show(user_input, headers)
        if bitlink != None:
            print('Битлинк', bitlink)
        else:
            print('Ошибка ввода!')
    else:
        clicks = shows_clicks(user_input, headers)
        if clicks != None:
            print(f'По вашей ссылке прошли: {clicks} раз(а)')
        else:
            print('Ошибка ввода!')


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')
    headers = {'Authorization': token}
    main(headers)
