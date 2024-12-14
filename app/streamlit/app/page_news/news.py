import streamlit as st
import requests

def render_page():
    st.header("Новости")
    
    api_url = "http://service_news:8002/news"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        st.success(f"Ответ от сервиса: {data['message']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")