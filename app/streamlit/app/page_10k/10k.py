import streamlit as st
import requests
import pandas as pd


def eda():
    '''
    Результаты разведовательного анализа данных.
    '''
    pass


@st.cache_data
def get_params():
    '''
    Получает параметры модели.
    '''
    api_url = 'http://service_10k:8001/get_params'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")
        return {}


def model_params():
    '''
    Параметры и гиперпараметры модели.
    '''
    st.image('eda_10k/ROC_AUC.png', caption='График ROC кривой')
    params = get_params()
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
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")
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
