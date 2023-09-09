import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        payload = {}
        headers = {
            "apikey": "6XpvyyBDpYUIxJiwEPWHOjebtbP8bBsM"
        }
        print('загрузка')
        r = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?symbols={sym_key}&base={base_key}",
                         headers=headers, data=payload)

        price_1 = json.loads(r.content)
        price = price_1.get('rates')
        price_2 = price[sym_key]
        text = f'Цена {amount} {base} в {sym} : {price_2}'
        return text