import data_download as dd
import data_plotting as dplt


def main():
    """
        Основная функция программы, которая управляет процессом получения данных о ценах акций,
        расчетом скользящего среднего, анализом колебаний цен, построением и сохранением графиков.

        Пользователь вводит тикер акции и период для данных, а также пороговое значение для колебаний цены в
        процентах после вывода средней цены закрытия. Программа загружает данные, рассчитывает скользящее среднее,
        выводит среднюю цену закрытия, анализирует колебания цен и строит график.

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

    # Calculate and display average price
    dd.calculate_and_display_average_price(stock_data)

    # Notify if there are strong fluctuations
    threshold = float(input("Введите пороговое значение для колебаний цены в процентах (например, 10 для 10%): "))
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()