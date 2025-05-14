import requests
from config import EXCHANGERATE_API_KEY


BASE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}"


class RatesFetcher:
    def fetch_rates(self):
        url = f"{BASE_URL}/latest/USD"
        try:
            response = requests.get(url)
            data = response.json()

            if data["result"] != "success":
                print("Ошибка при загрузке валют:", data)
                return {}

            return data["conversion_rates"]
        except Exception as e:
            print("Ошибка запроса:", e)
            return {}
        

class CurrencyConverter:
    def get_format_of_converted_currency(self, amount, from_currency, to_currency):
        self.__raise_if_amount_invalid(amount)
        
        amount = float(amount)

        try:
            result = self.__calculate_result(amount, from_currency, to_currency)
            output = f"{amount} {from_currency} = {round(result, 2)} {to_currency}"
            return output
        except Exception as e:
            raise InternalError('Внутрення ошибка программы')
        
    def __raise_if_amount_invalid(self, amount):
        if not amount.replace('.', '', 1).isdigit():
            raise ValueError('Введите корректную сумму')

    def __calculate_result(self, amount, from_currency, to_currency):
        if amount == 0: 
            return 0
        else: 
            return self.__fetch_converted_currency(amount, from_currency, to_currency)

    def __fetch_converted_currency(self, amount, from_currency, to_currency):
        url = f"{BASE_URL}/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        if data["result"] != "success":
            raise InternalError('Не удалось выполнить преобразование')

        rate = data["conversion_rates"].get(to_currency)
        if rate is None:
            raise ValueError('Некорректная валюта')

        return amount * rate


class InternalError(Exception):
    def __init__(self, msg: str):
        self.__msg = msg

    def __str__(self):
        return self.__msg
