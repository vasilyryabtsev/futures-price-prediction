import streamlit as st
import requests

def render_page():
    st.header("Анализ Twitter")
    
    api_url = "http://service_twitter:8004/twitter"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        st.success(f"Ответ от сервиса: {data['message']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")