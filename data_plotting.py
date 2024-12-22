import matplotlib.pyplot as plt  # Импортируем matplotlib для построения графиков
import pandas as pd  # Импортируем pandas для работы с данными
import matplotlib.dates as mdates  # Импортируем для форматирования дат на графиках


def create_and_save_plot(data, ticker, period=None, use_date_range=False, filename=None):
    """
    Создает и сохраняет график цен акций, скользящего среднего, RSI и MACD.

    Параметры:
        data: DataFrame с данными о ценах акций.
        ticker (str): Тикер акции.
        period (str, optional): Период для данных (используется для имени файла, если use_date_range=False).
        use_date_range (bool, optional): Флаг, указывающий, что используется диапазон дат (по умолчанию False).
        filename (str, optional): Имя файла для сохранения графика (по умолчанию None).
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)  # Создаем фигуру и 3
    # подграфика, разделяющие ось x

    # График цены и скользящего среднего
    if 'Date' not in data:  # Проверяем, есть ли колонка Date в DataFrame
        if pd.api.types.is_datetime64_any_dtype(data.index):  # Если нет, проверяем является ли индекс DataFrame датой
            dates = data.index.to_numpy()  # Если является, преобразуем индекс в массив numpy
            ax1.plot(dates, data['Close'].values, label='Close Price')  # Строим график цены закрытия на первом
            # подграфике
            if 'Moving_Average' in data.columns:  # Проверяем, есть ли колонка Moving_Average
                ax1.plot(dates, data['Moving_Average'].values, label='Moving Average')  # Строим график скользящего
                # среднего на первом подграфике
            ax1.xaxis.set_major_locator(mdates.AutoDateLocator())  # Локатор автоматически определяет наиболее
            # подходящие интервалы для основных делений на оси времени.
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Устанавливаем формат дат на оси x

        else:  # Если индекс не является датой, выводим ошибку
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:  # Если колонка Date есть в DataFrame
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):  # Проверяем является ли колонка Date датой
            data['Date'] = pd.to_datetime(data['Date'])  # Если нет, преобразуем в формат даты
        ax1.plot(data['Date'], data['Close'],
                 label='Close Price')  # Строим график цены закрытия на первом подграфике
        if 'Moving_Average' in data.columns:  # Проверяем, есть ли колонка Moving_Average
            ax1.plot(data['Date'], data['Moving_Average'],
                     label='Moving Average')  # Строим график скользящего среднего на первом подграфике
        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())  # Автоматически устанавливаем локатор для дат
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Устанавливаем формат дат на оси x
    ax1.set_title(f"{ticker} Цена акций с течением времени")  # Устанавливаем заголовок первого подграфика
    ax1.set_ylabel("Цена")  # Устанавливаем подпись оси y для первого подграфика
    ax1.legend()  # Добавляем легенду на первом подграфике
    ax1.grid(True)  # Включаем сетку на первом подграфике

    # График RSI
    if 'RSI' in data.columns:  # Проверяем, есть ли колонка RSI
        ax2.plot(dates, data['RSI'], label='RSI', color='orange')  # Строим график RSI на втором подграфике
        ax2.axhline(70, color='red', linestyle='--', alpha=0.5)  # Добавляем горизонтальную линию на уровне 70
        ax2.axhline(30, color='green', linestyle='--', alpha=0.5)  # Добавляем горизонтальную линию на уровне 30
        ax2.set_ylabel("RSI")  # Устанавливаем подпись оси y для второго подграфика
        ax2.legend()  # Добавляем легенду на втором подграфике
        ax2.grid(True)  # Включаем сетку на втором подграфике

    # График MACD
    if 'MACD' in data.columns and 'Signal' in data.columns and 'Histogram' in data.columns:  # Проверяем, есть ли
        # столбцы MACD, Signal и Histogram
        ax3.plot(dates, data['MACD'], label='MACD', color='blue')  # Строим график MACD на третьем подграфике
        ax3.plot(dates, data['Signal'], label='Signal',
                 color='red')  # Строим график сигнальной линии на третьем подграфике
        ax3.bar(dates, data['Histogram'], label='Histogram',
                color='grey')  # Строим гистограмму на третьем подграфике
        ax3.set_ylabel("MACD")  # Устанавливаем подпись оси y для третьего подграфика
        ax3.legend()  # Добавляем легенду на третьем подграфике
        ax3.grid(True)  # Включаем сетку на третьем подграфике

    plt.tight_layout()  # Устанавливаем layout чтобы графики не перекрывались

    if filename is None:  # Проверяем, передано ли имя файла
        if use_date_range:
            start_date = data.index.min().strftime('%Y-%m-%d')
            end_date = data.index.max().strftime('%Y-%m-%d')
            filename = f"{ticker}_{start_date}_to_{end_date}_stock_indicators_chart.png"  # Формируем имя файла если
            # сами указали диапазон дат
        else:
            filename = f"{ticker}_{period}_stock_indicators_chart.png"  # Формируем имя файла по умолчанию
    plt.savefig(filename)  # Сохраняем график в файл
    print(f"График сохранен как {filename}")  # Выводим сообщение о сохранении графика
