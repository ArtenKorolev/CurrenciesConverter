import tkinter as tk
from tkinter import ttk
from typing import List
from core import InternalError


class TkinterWindow:
    def __init__(self, rates_fetcher, converted_currency_fetcher):
        self.__converted_currency_fetcher = converted_currency_fetcher
        self.__root = tk.Tk()
        self.__root.title("Конвертер валют")
        self.__root.geometry("400x450")

        self.__label_result = None
        self.__entry_amount = None
        self.__combo_from = None
        self.__combo_to = None
        self.__history_listbox = None

        self.__init_interface(rates_fetcher)

    def __init_interface(self, rates_fetcher):
        try:
            currencies = list(rates_fetcher.fetch_rates().keys())
            default_message = ""
        except InternalError as e:
            currencies = []
            default_message = f"Ошибка загрузки: {str(e)}"

        self.__create_label("Сумма:")
        self.__entry_amount = self.__create_entry()

        self.__create_label("Из валюты:")
        self.__combo_from = self.__create_combobox(currencies, "USD")

        self.__create_label("В валюту:")
        self.__combo_to = self.__create_combobox(currencies, "EUR")

        tk.Button(self.__root, text="Конвертировать", command=self.__handle_convert).pack(pady=10)

        self.__label_result = tk.Label(self.__root, text=default_message, font=("Arial", 12, "bold"))
        self.__label_result.pack(pady=10)

        self.__create_label("История:")
        self.__history_listbox = tk.Listbox(self.__root, height=10)
        self.__history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def __create_label(self, text: str):
        tk.Label(self.__root, text=text).pack(pady=5)

    def __create_entry(self) -> tk.Entry:
        entry = tk.Entry(self.__root)
        entry.pack()
        return entry

    def __create_combobox(self, values: List[str], default: str) -> ttk.Combobox:
        combo = ttk.Combobox(self.__root, values=values, state="readonly")
        if default in values:
            combo.set(default)
        elif values:
            combo.set(values[0])
        combo.pack()
        return combo

    def __handle_convert(self):
        amount = self.__entry_amount.get().strip()
        from_currency = self.__combo_from.get()
        to_currency = self.__combo_to.get()

        if not amount:
            self.__label_result.config(text="Введите сумму.")
            return

        try:
            result_text = self.__converted_currency_fetcher.get_format_of_converted_currency(
                amount, from_currency, to_currency
            )
            self.__label_result.config(text=result_text)
            self.__history_listbox.insert(0, result_text)
        except (InternalError, ValueError) as e:
            self.__label_result.config(text=f"Ошибка: {str(e)}")

    def run(self):
        self.__root.mainloop()
