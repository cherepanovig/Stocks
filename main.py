import data_download as dd
import data_plotting as dplt
from datetime import datetime  # Добавляем модуль для работы с датой и временем
import matplotlib.pyplot as plt  # Для запроса видов стиля графика


def main():
    """
        Основная функция программы, которая управляет процессом получения данных о ценах акций,
        расчетом скользящего среднего, анализом колебаний цен, построением и сохранением графиков.

        Пользователь вводит тикер акции и период для данных, а также пороговое значение для колебаний цены в
        процентах после вывода средней цены закрытия. Программа загружает данные, рассчитывает скользящее среднее,
        выводит среднюю цену закрытия, анализирует колебания цен, рассчитывает MACD, RSI и строит график. Также добавлена функция,
        которая позволяет сохранять загруженные данные об акциях в CSV файл. Доступен выбор стиля графиков.

    """

    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), "
        "MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, "
        "макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    # period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    use_date_range = input("Хотите указать диапазон дат (да/нет)? ").lower()
    if use_date_range == "да":
        start_date_str = input("Введите дату начала в формате ГГГГ-ММ-ДД (например, 2024-01-01): ")
        end_date_str = input("Введите дату окончания в формате ГГГГ-ММ-ДД (например, 2024-03-01): ")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        # Вызов функции fetch_stock_data для получения данных
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)

    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")

        # Вызов функции fetch_stock_data для получения данных
        stock_data = dd.fetch_stock_data(ticker, period=period)

    if stock_data.empty:
        print("Не удалось получить данные для указанных параметров.")
        return

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Вызов функции для рассчета средней цены закрытия
    dd.calculate_and_display_average_price(stock_data)

    # Вызов функции для расчёта стандартного отклонения цены закрытия акции
    dd.calculate_and_display_standard_deviation(stock_data)

    threshold = float(input("Введите пороговое значение для колебаний цены в процентах (например, 10 для 10%): "))
    # Вызов функции для рассчета колебаний цены акции
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Вызываем функцию add_rsi для расчета RSI
    stock_data = dd.add_rsi(stock_data)

    # Вызываем функцию add_macd для расчета MACD
    stock_data = dd.add_macd(stock_data)

    # Генерация имени файла на основе тикера и текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{ticker}_{current_date}_data.csv"

    # Сохранение данных в CSV
    dd.export_data_to_csv(stock_data, filename)
    # print(f"Данные сохранены в файл: {filename}")

    # # Сохраняем данные в CSV-файл
    # csv_filename = input("Введите имя файла для сохранения данных (например, 'stock_data.csv'): ")
    # dd.export_data_to_csv(stock_data, csv_filename)

    # Получение доступных стилей графиков
    available_styles = plt.style.available
    print("Доступные стили графиков:", available_styles)

    # Запрос выбора стиля у пользователя
    selected_style = input(f"Введите желаемый стиль (по умолчанию 'default'): ")
    if selected_style not in available_styles:
        selected_style = 'default'

    # Plot the data
    # dplt.create_and_save_plot(stock_data, ticker, period)
    if use_date_range == "да":
        dplt.create_and_save_plot(stock_data, ticker, period=None, use_date_range=True, plot_style=selected_style)
    else:
        dplt.create_and_save_plot(stock_data, ticker, period=period, use_date_range=False, plot_style=selected_style)


if __name__ == "__main__":
    main()
