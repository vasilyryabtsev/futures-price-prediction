import importlib
import streamlit as st
import logging
import logging.config
import config

logging.config.dictConfig(config.LOGGING_CONFIG)

logger = logging.getLogger('service_streamlit')

def main():
    '''
    Главная страница.
    '''
    st.set_page_config(page_title="Навигация по страницам", layout="wide")

    st.title("Future price prediction")

    logger.info("Запущен Streamlit-приложение")

    # Словарь страниц с указанием модулей
    pages = {
        "Годовой отчет": "page_10k.10k",
        "Twitter": "page_twitter.twitter"
    }

    # Выпадающий список для выбора страницы
    selected_page = st.selectbox("Выберите тип текста", options=pages.keys())
    logger.info("Пользователь выбрал: %s", selected_page)

    # Динамическое импортирование и вызов функции страницы
    module = importlib.import_module(pages[selected_page])
    module.render_page()


if __name__ == "__main__":
    main()
