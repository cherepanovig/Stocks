import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    """
    Загружает данные о ценах акций для указанного тикера и периода.

    Параметры:
        ticker (str): Тикер акции (например, 'AAPL' для Apple Inc).
        period (str, optional): Период для данных (по умолчанию '1mo' для одного месяца).

    Возвращает:
        data: DataFrame с данными о ценах акций.
    """
    stock = yf.Ticker(ticker)  # Создаем объект Ticker из yfinance, он представляет акцию с введенным тикером
    data = stock.history(period=period)  # Получаем данные для этой акции за введенный период
    # print(data.to_string(index=False))  # метод позволяет выводить из DataFrame все столбцы
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляет столбец с скользящим средним к DataFrame с данными о ценах акций.

    Параметры:
        data: DataFrame с данными о ценах акций.
        window_size (int, optional): Размер окна для расчета скользящего среднего (по умолчанию 5).

    Возвращает:
        data: DataFrame с добавленным столбцом 'Moving_Average'.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    # print(data.to_string(index=False))  # метод позволяет выводить из DataFrame все столбцы
    return data


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций.

    Параметры:
        data: DataFrame с данными о ценах акций.
    """
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: Переданные данные не являются DataFrame.")
        return

    if 'Close' not in data.columns:
        print("Ошибка: В DataFrame отсутствует колонка 'Close'.")
        return

    average_price = data['Close'].mean()  # Вычисляем среднее значение по столбцу 'Close'
    print(f"Средняя цена закрытия: {average_price:.2f}")


def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

    Параметры:
        data: DataFrame с данными о ценах акций.
        threshold (float): Введенное пороговое значение в процентах для определения сильных колебаний.
    """
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: Переданные данные не являются DataFrame.")
        return

    if 'Close' not in data.columns:
        print("Ошибка: В DataFrame отсутствует колонка 'Close'.")
        return

    # Вычисляем максимальное и минимальное значения цены закрытия
    max_price = data['Close'].max()
    min_price = data['Close'].min()

    # Вычисляем разницу в процентах
    price_fluctuation = ((max_price - min_price) / min_price) * 100

    # Сравниваем разницу с пороговым значением
    if price_fluctuation > threshold:
        print(f"Внимание! Цена акций колебалась более чем на {price_fluctuation:.2f}%, что превышает порог в "
              f"{threshold}%.")
    else:
        print(f"Цена акций колебалась на {price_fluctuation:.2f}%, что находится в пределах допустимого порога в "
              f"{threshold}%.")


def export_data_to_csv(data, filename):
    """
    Экспортирует данные о ценах акций в CSV файл.

    Параметры:
        data: DataFrame с данными о ценах акций.
        filename (str): Имя файла для сохранения данных в формате CSV.
    """
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: Переданные данные не являются DataFrame.")
        return

    try:
        data.to_csv(filename, index=True)  # Сохраняем данные в CSV файл с индексами
        print(f"Данные успешно сохранены в файл: {filename}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении данных в файл: {e}")


def add_rsi(data, period=14):
    """
    Добавляет столбец с индексом относительной силы (RSI) к DataFrame.

    Параметры:
        data: DataFrame с данными о ценах акций.
        period (int, optional): Период для расчета RSI (по умолчанию 14).

    Возвращает:
        data: DataFrame с добавленным столбцом 'RSI'.
        Или None, если произошла ошибка.
    """
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: Переданные данные не являются DataFrame.")
        return None

    if 'Close' not in data.columns:
        print("Ошибка: В DataFrame отсутствует колонка 'Close'.")
        return None
    delta = data['Close'].diff()  # Расчёт изменения цены закрытия
    up = delta.clip(lower=0)  # Значения роста (акция росла)
    down = -1 * delta.clip(upper=0)  # Значения падения (акция падала)
    average_up = up.rolling(window=period).mean()  # Среднее значение роста
    average_down = down.rolling(window=period).mean()  # Среднее значение падения
    rs = average_up / average_down  # Отношение роста к падению
    rsi = 100 - (100 / (1 + rs))  # Вычисляем RSI
    data['RSI'] = rsi  # Добавляем столбец RSI в DataFrame
    return data


def add_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Добавляет столбцы MACD, Signal и Histogram к DataFrame.

    Параметры:
        data: DataFrame с данными о ценах акций.
        fast_period (int, optional): Период для быстрого EMA (по умолчанию 12).
        slow_period (int, optional): Период для медленного EMA (по умолчанию 26).
        signal_period (int, optional): Период для сигнальной линии EMA (по умолчанию 9).

    Возвращает:
        data: DataFrame с добавленными столбцами 'MACD', 'Signal' и 'Histogram'.
        Или None, если произошла ошибка.
    """
    if not isinstance(data, pd.DataFrame):
        print("Ошибка: Переданные данные не являются DataFrame.")
        return None

    if 'Close' not in data.columns:
        print("Ошибка: В DataFrame отсутствует колонка 'Close'.")
        return None
    fast_ema = data['Close'].ewm(span=fast_period, adjust=False).mean()  # Быстрая EMA
    slow_ema = data['Close'].ewm(span=slow_period, adjust=False).mean()  # Медленная EMA
    macd = fast_ema - slow_ema  # MACD = разница между быстрой и медленной EMA
    signal = macd.ewm(span=signal_period, adjust=False).mean()  # Сигнальная линия
    histogram = macd - signal  # Гистограмма MACD
    # Добавляем столбец MACD, Signal, Histogram
    data['MACD'] = macd
    data['Signal'] = signal
    data['Histogram'] = histogram
    return data
