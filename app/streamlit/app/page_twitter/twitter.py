import streamlit as st
import requests
import pandas as pd
from collections import Counter
import re

def analyze_text_file(user_input):
    """
    Выполняет базовый анализ текстового файла.
    """
    st.title("Анализ популярных слов")
    if user_input:
        words = re.findall(r'\b\w+\b', user_input.lower())
        word_counts = Counter(words)
        word_freq_df = pd.DataFrame(word_counts.items(), columns=["Слово", "Частота"]).sort_values(by="Частота", ascending=False)
        st.subheader("Топ-10 популярных слов:")
        st.dataframe(word_freq_df.head(10))
        st.subheader("Гистограмма частот:")
        st.bar_chart(word_freq_df.set_index("Слово").head(10))
def print_eda():
    st.header("Информация о модели")
    st.image("/code/app/eda_twitter/cnt_twitts.png", caption="Кол-во твитов по годам")
    st.image("/code/app/eda_twitter/tags.png", caption="Самые популярные хэштеги")
    st.image("/code/app/eda_twitter/title.png", caption="Самые популярные слова в названиях")
    st.image("/code/app/eda_twitter/words_title.png", caption="Самые популярные слова в названиях")

def giper_param():
    if "show_image" not in st.session_state:
        st.session_state.show_image = False

    if st.button("Открыть гиперпараметры"):
        st.session_state.show_image = not st.session_state.show_image

    # Отображение или скрытие изображения
    if st.session_state.show_image:
        st.header("Гиперпараметры")
        st.write("Параметр регуляризации: C=1.77")
        st.image("/code/app/eda_twitter/metrics.png", caption="Метрики качества модели")

def upload_dataset():
    user_input = st.text_input("Введите текст:", placeholder="Например, введите свой пост")
    if user_input:
        analyze_text_file(user_input)

        print_eda()
        giper_param()

        api_url = "http://service_twitter:8004/report_prediction"
        try:
            input_data = {"text": user_input}
            response = requests.post(api_url, json=input_data)
            response.raise_for_status()
            st.header("Результат прогноза")
            st.json(response.json())
            return response
        except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться к сервису: {e}")
    return None


def render_page():
    st.title("Streamlit-приложение для анализа и моделей")

    # Загрузка данных
    data = upload_dataset()