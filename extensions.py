import requests
import json
from config import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Введены одинаковые вылюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        try:
            keys[quote]
        except KeyError:
            raise APIException(f'Указанная валюта "{quote}" отсутствует в списке конвертора')

        try:
            keys[base]
        except KeyError:
            raise APIException(f'Указанная валюта "{base}" отсутствует в списке конвертора')

        try:
            amount < 0
        except ValueError:
            raise APIException(f'Количество валюты меньше нуля')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        total_base = amount * json.loads(r.content)[keys[quote]]

        return total_base
