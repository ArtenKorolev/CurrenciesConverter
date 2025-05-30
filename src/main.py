from gui import TkinterWindow
from core import RatesFetcher, CurrencyConverter


if __name__ == '__main__':
    window = TkinterWindow(RatesFetcher(), CurrencyConverter())
    window.run()
