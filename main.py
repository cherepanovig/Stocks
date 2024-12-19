import data_download as dd
import data_plotting as dplt
from datetime import datetime  # Добавляем модуль для работы с датой и временем


def main():
    """
        Основная функция программы, которая управляет процессом получения данных о ценах акций,
        расчетом скользящего среднего, анализом колебаний цен, построением и сохранением графиков.

        Пользователь вводит тикер акции и период для данных, а также пороговое значение для колебаний цены в
        процентах после вывода средней цены закрытия. Программа загружает данные, рассчитывает скользящее среднее,
        выводит среднюю цену закрытия, анализирует колебания цен и строит график. Также добавлена функция,
        которая позволяет сохранять загруженные данные об акциях в CSV файл.

    """

    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), "
        "MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, "
        "макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Вызов функции для рассчета средней цены закрытия
    dd.calculate_and_display_average_price(stock_data)

    threshold = float(input("Введите пороговое значение для колебаний цены в процентах (например, 10 для 10%): "))
    # Вызов функции для рассчета колебаний цены акции
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Генерация имени файла на основе тикера и текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{ticker}_{current_date}_data.csv"

    # Сохранение данных в CSV
    dd.export_data_to_csv(stock_data, filename)
    # print(f"Данные сохранены в файл: {filename}")

    # # Сохраняем данные в CSV-файл
    # csv_filename = input("Введите имя файла для сохранения данных (например, 'stock_data.csv'): ")
    # dd.export_data_to_csv(stock_data, csv_filename)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()