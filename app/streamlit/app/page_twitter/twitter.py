import streamlit as st
import requests
import pandas as pd

@st.cache_data
def upload_data(path: str) -> pd.DataFrame:
    '''
    Загрузка датасета.
    '''
    return pd.read_csv(path)

@st.cache_data
def get_unique(col: pd.Series) -> pd.DataFrame:
    '''
    Возвращает уникальные значения атрибута.
    '''
    return pd.DataFrame({col.name: col.unique()})

def show_images():
    '''
    Показывает графики.
    '''

    images = [
        'eda_twitter/tweets_year.png',
        'eda_twitter/words_cloud.png'
    ]

    check_plot = st.checkbox('Показать графики')
    if check_plot:
        st.image(images[0])
        st.image(images[1])
        
@st.cache_data
def class_prop(target: pd.Series) -> pd.DataFrame:
    '''
    Возвращает соотношение классов.
    '''
    return target.value_counts(normalize=True).to_frame()

def eda():
    '''
    Результаты разведовательного анализа данных.
    '''
    st.header("EDA")
    
    data = upload_data('page_twitter/final.csv')
    data = data[['username', 'ticker', 'text', 'year', 'month', 'day', '1_day_after']]
    
    st.write(data)
    st.write(f'''
    Для обучения модели было отобрано {data.shape[0]} твита инфлюенсеров из финансовой сферы по выбранным тикерам.
    Таргетом является столбец 1_day_after, т.е. вырастет цена акции на следующий день после публикации твита или нет.
             ''')
    st.write("Список инфлюенсеров:")
    st.write(get_unique(data['username']))
    st.write("Список тикеров:")
    st.write(get_unique(data['ticker']))
    
    show_images()
    
    st.write('Соотношение классов:')
    st.write(class_prop(data['1_day_after']))
    
def model_params():
    '''
    Гиперпараметры модели.
    '''
    pass

@st.cache_data
def get_predict(text):
    '''
    Возвращает прогноз модели.
    '''
    api_url = "http://service_twitter:8004/report_prediction"
    input_data = {"text": text}
    try:
        response = requests.post(api_url, json=input_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")
        return dict()
    
def model_prediction():
    '''
    Прогноз модели.
    '''
    user_input = st.text_input('Введите текст:', placeholder='The chance of $MSFT winning an appeal is slim.')
    if user_input:
        pred = get_predict(user_input)
        if len(pred) > 0:
            st.write(f"🟥: {pred['negative_probability']}")
            st.write(f"🟩: {pred['positive_probability']}")
        else:
            st.write(f"🟥: 0.0")
            st.write(f"🟩: 0.0")

def render_page():
    check_eda = st.checkbox('EDA')
    if check_eda:
        eda()
        
    check_params = st.checkbox('Параметры модели')
    if check_params:
        model_params()
        
    check_prediction = st.checkbox('Прогноз модели')
    if check_prediction:
        model_prediction()