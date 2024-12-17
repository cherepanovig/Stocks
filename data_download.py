import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    #print(data.to_string(index=False))  # метод позволяет выводить из DataFrame все столбцы
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """Вычисляет и выводит среднюю цену закрытия акций."""
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: Переданные данные не являются DataFrame.")
        return

    if 'Close' not in data.columns:
        print("Ошибка: В DataFrame отсутствует колонка 'Close'.")
        return

    average_price = data['Close'].mean()  # Вычисляем среднее значение по столбцу 'Close'
    print(f"Средняя цена закрытия: {average_price:.2f}")