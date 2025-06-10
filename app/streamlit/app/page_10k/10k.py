import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger('page_10k')


@st.cache_data
def upload_data(path: str) -> pd.DataFrame:
    '''
    Загрузка датасета.
    '''
    logger.info('Получены данные')

    return pd.read_csv(path)


def plot_MDA_distribution(data):
    """
    Функция для построения гистограммы распределения длины раздела MDA.
    """
    plt.figure(figsize=(8, 5))
    plt.hist(data['full_content_length'], bins=20, alpha=0.7)
    plt.title('Распределение длины раздела MDA отчетов 10-K')
    plt.xlabel('Длина (символов)')
    plt.grid()
    
    logger.info('Построена гистограмма распределения')

    return plt


def boxplot_MDA_length(data):
    """
    Функция для построения boxplot для длины раздела MDA.
    """
    plt.figure(figsize=(8, 5))
    plt.boxplot(data['full_content_length'])
    plt.title('Длина раздела MDA отчетов 10-K в зависимости от значения таргета')
    plt.ylabel('Длина (символов)')
    plt.grid()

    logger.info('Построен boxplot')

    return plt


def hist_target_dist(data):
    """
    Функция для построения гистограммы распределения значений с разной целевой переменной.
    """
    plt.figure(figsize=(8, 5))
    plt.hist(data['target_10_index'], bins=3, alpha=0.7)
    plt.title('Распределение целевой переменной')
    plt.xlabel('Количество наблюдений')
    plt.grid()
    
    logger.info('Построена гистограмма распределения значений с разной целевой переменной')

    return plt


def get_unique_tickers(data):
    '''
    Возвращает уникальные тикеры и количество отчетов по ним.
    '''
    report_counts = data['ticker'].value_counts().reset_index()
    report_counts.columns = ['Тикер', 'Количество отчетов']

    logger.info('Возврат уникальных тикеров')

    return report_counts


def eda():
    '''
    Результаты разведовательного анализа данных.
    '''
    logger.info('Вызван EDA')

    st.header("EDA")

    data = upload_data('page_10k/final.csv')
    data['full_content_length'] = data['MDA'].apply(len)
    st.write('1. Список компаний, по которым проводится анализ')
    tickers = get_unique_tickers(data)
    st.table(tickers)
    st.write('2. Распределение длины раздела MDA отчетов 10K')
    fig_len = plot_MDA_distribution(data)
    st.pyplot(fig_len)
    st.write('3. Boxplot длины раздела MDA отчетов 10K по таргету')
    bp_len = boxplot_MDA_length(data)
    st.pyplot(bp_len)
    st.write('4. Распределение целевой переменной')
    dist_len = hist_target_dist(data)
    st.pyplot(dist_len)


@st.cache_data
def get_params():
    '''
    Получает параметры модели.
    '''
    api_url = 'http://service_10k:8001/get_params'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        logger.info('Получены параметры модели')
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")
        logger.error(f"Не удалось получить параметры: {str(e)}")
        return {}


def model_params():
    '''
    Параметры и гиперпараметры модели.
    '''
    st.image('eda_10k/ROC_AUC.png', caption='График ROC кривой')
    params = get_params()
    logger.info('Отображены параметры модели')
    if params:
        param_df = pd.DataFrame(list(params.items()),
                                columns=["Параметр", "Значение"])

        st.table(param_df)


def file_prev(uploaded_file):
    '''
    Вывод на экран загруженного текста.
    '''
    content = uploaded_file.read().decode("utf-8")

    st.text_area(uploaded_file.name, content, height=300)


@st.cache_data
def get_predict(uploaded_file):
    '''
    Возвращает прогноз модели.
    '''
    api_url = "http://service_10k:8001/report_prediction"
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()
        logger.info('Возвращен прогноз')
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")
        logger.error(f"Не удалось вернуть прогноз: {str(e)}")
        return {}


def model_prediction():
    '''
    Прогноз модели.
    '''
    uploaded_file = st.file_uploader('Выберите файл', type='txt')
    if uploaded_file:
        file_prev(uploaded_file)
        pred = get_predict(uploaded_file)
        if len(pred) > 0:
            st.write(f"🟥: {pred['negative_probability']}")
            st.write(f"🟩: {pred['positive_probability']}")
        else:
            st.write("🟥: 0.0")
            st.write("🟩: 0.0")
    logger.info('Отображен прогноз')


def render_page():
    '''
    Рендерит страницу.
    '''
    check_eda = st.checkbox('EDA')
    if check_eda:
        eda()

    check_params = st.checkbox('Параметры модели')
    if check_params:
        model_params()

    check_prediction = st.checkbox('Прогноз модели')
    if check_prediction:
        model_prediction()
