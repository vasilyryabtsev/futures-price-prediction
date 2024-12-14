import importlib
import streamlit as st

def main():
    st.set_page_config(page_title="Навигация по страницам", layout="wide")

    st.title("Future price prediction")

    # Словарь страниц с указанием модулей
    pages = {
        "10K Page": "page_10k.10k",
        "News Page": "page_news.news",
        "Reddit Page": "page_reddit.reddit",
        "Twitter Page": "page_twitter.twitter"
    }

    # Выпадающий список для выбора страницы
    selected_page = st.selectbox("Выберите страницу", options=pages.keys())

    # Динамическое импортирование и вызов функции страницы
    module = importlib.import_module(pages[selected_page])
    module.render_page()

if __name__ == "__main__":
    main()
