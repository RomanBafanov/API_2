from typing import Any
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import requests


BODY = {}

URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def count_clicks(token, link) -> Any:
    headers = {'Authorization': token}
    url = f'{URL}/{link}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def shorten_link(token, body) -> Any:
    headers = {'Authorization': token}
    response = requests.post(URL, headers=headers, json=body)
    response.raise_for_status()

    return response.json()['link']


def is_bitlink(token, link) -> bool:
    headers = {'Authorization': token}
    response = requests.get(f'{URL}/{link}', headers=headers)
    if response.raise_for_status():
        return True
    else:
        return False


def main() -> Any:
    load_dotenv()
    token = os.getenv('BITLINK_TOKEN')
    user_input = input('Введите ссылку ')
    parsed_url = urlparse(user_input)
    print(parsed_url)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    if is_bitlink(token, link):
        print(link)
        BODY['long_url'] = link
        try:
            bitlink = shorten_link(token, BODY)
        except requests.exceptions.HTTPError:
            print('Ошибка ввода при уменьшении!')
        else:
            print('Битлинк', bitlink)
    else:
        try:
            clicks = count_clicks(token, link)
        except requests.exceptions.HTTPError:
            print('Ошибка ввода при поиске кликов!')
        else:
            print(f'По вашей ссылке прошли: {clicks} раз(а)')


if __name__ == '__main__':
    main()
