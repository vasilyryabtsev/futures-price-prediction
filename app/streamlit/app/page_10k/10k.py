import streamlit as st
import requests
import pandas as pd

def analyze_text_file(file):
    """
    Выполняет базовый анализ текстового файла.
    """
    # Чтение содержимого файла
    content = file.read().decode("utf-8")
    # Подсчет слов
    words = content.split()
    word_count = len(words)
    # Подсчет строк
    line_count = content.count('\n') + 1
    # Подсчет символов
    char_count = len(content)

    st.subheader("EDA")
    st.write(f"Количество слов: {word_count}")
    st.write(f"Количество строк: {line_count}")
    st.write(f"Количество символов: {char_count}")
def print_eda():
    st.header("Информация о модели")
    st.image("/code/app/eda_10k/eda.005.jpeg")
    st.image("/code/app/eda_10k/eda.008.jpeg")
    st.image("/code/app/eda_10k/eda.009.jpeg")

def giper_param():
    if "show_image_1" not in st.session_state:
        st.session_state.show_image_1 = False

    if st.button("Открыть гиперпараметры"):
        st.session_state.show_image_1 = not st.session_state.show_image_1

    # Отображение или скрытие изображения
    if st.session_state.show_image_1:
        api_url = "http://service_10k:8001/get_params"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            st.header("Гиперпараметры")
            st.json(response.json())
            st.image("/code/app/eda_10k/ROC_AUC.png", caption="График ROC кривой")
        except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться к сервису: {e}")

def upload_dataset():
    st.sidebar.header("Загрузка данных")
    uploaded_file = st.sidebar.file_uploader("Загрузите ваш dataset (TXT)", type=["txt"])
    if uploaded_file:
        analyze_text_file(uploaded_file)
        file_content = uploaded_file.getvalue().decode("utf-8")

        preview = file_content[:300]
        st.header("Превью содержимого файла:")
        st.text(preview)
        print_eda()
        giper_param()

        api_url = "http://service_10k:8001/report_prediction"
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            st.header("Результат прогноза")
            st.json(response.json())
            return response
        except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться к сервису: {e}")
    return None


def render_page():
    # Загрузка данных
    data = upload_dataset()




