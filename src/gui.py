import tkinter as tk
from tkinter import ttk
from use_cases import InternalError


class TkinterWindow:
    def __init__(self, rates_fetcher, converted_currency_fetcher):
        self.__converted_currency_fetcher = converted_currency_fetcher
        self.__root = tk.Tk()
        self.__root.title("Конвертер валют")
        self.__root.geometry("400x450")

        text = ''
        try:
            currencies = list(rates_fetcher.fetch_rates().keys())
        except InternalError as e:
            currencies=[]
            text = str(e)

        tk.Label(self.__root, text="Сумма:").pack(pady=5)
        self.__entry_amount = tk.Entry(self.__root)
        self.__entry_amount.pack()

        tk.Label(self.__root, text="Из валюты:").pack(pady=5)
        self.__combo_from = ttk.Combobox(self.__root, values=currencies, state="readonly")
        self.__combo_from.set("USD")
        self.__combo_from.pack()

        tk.Label(self.__root, text="В валюту:").pack(pady=5)
        self.__combo_to = ttk.Combobox(self.__root, values=currencies, state="readonly")
        self.__combo_to.set("EUR")
        self.__combo_to.pack()

        tk.Button(self.__root, text="Конвертировать", command=self.__handle_convert).pack(pady=10)

        self.__label_result = tk.Label(self.__root, text=text, font=("Arial", 12, "bold"))
        self.__label_result.pack(pady=10)

        tk.Label(self.__root, text="История:").pack()
        self.__history_listbox = tk.Listbox(self.__root, height=10)
        self.__history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def __handle_convert(self):
        amount = self.__entry_amount.get()
        from_currency = self.__combo_from.get()
        to_currency = self.__combo_to.get()

        try:
            result_text = self.__converted_currency_fetcher.get_format_of_converted_currency(amount, from_currency, to_currency)
            self.__label_result.config(text=result_text)
            self.__history_listbox.insert(0, result_text)
        except InternalError as e:
            self.__label_result.config(text=str(e))
        except ValueError as ve:
            self.__label_result.config(text=str(ve))

    def run(self):
        self.__root.mainloop()
