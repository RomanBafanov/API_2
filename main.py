from typing import Any
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import requests
import argparse


URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def count_clicks(token, link) -> Any:
    headers = {'Authorization': token}
    url = f'{URL}/{link}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def shorten_link(token, user_input) -> Any:
    headers = {'Authorization': token}
    body = {'long_url': user_input}
    response = requests.post(URL, headers=headers, json=body)
    response.raise_for_status()

    return response.json()['link']


def is_bitlink(token, link) -> bool:
    headers = {'Authorization': token}
    response = requests.get(f'{URL}/{link}', headers=headers)

    return response.ok


def main() -> Any:
    parser = argparse.ArgumentParser(
        description='Программа даёт возможность сократить ссылку и подсчитать колличество посещения короткой ссылки: '
                    'python main.py ваша ссылка'
    )
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    user_input = args.link
    parsed_url = urlparse(user_input)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    if is_bitlink(token, link):
        try:
            clicks = count_clicks(token, link)
        except requests.exceptions.HTTPError:
            print('Ошибка ввода при поиске кликов!')
        else:
            print(f'По вашей ссылке прошли: {clicks} раз(а)')
    else:
        try:
            bitlink = shorten_link(token, user_input)
        except requests.exceptions.HTTPError:
            print('Ошибка ввода при уменьшении!')
        else:
            print('Битлинк', bitlink)


if __name__ == '__main__':
    main()
