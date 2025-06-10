import streamlit as st
import requests
import pandas as pd
import logging


logger = logging.getLogger('page_twitter')

@st.cache_data
def upload_data(path: str) -> pd.DataFrame:
    '''
    Загрузка датасета.
    '''
    logger.info('Получены данные')

    return pd.read_csv(path)


@st.cache_data
def get_unique(col: pd.Series) -> pd.DataFrame:
    '''
    Возвращает уникальные значения атрибута.
    '''
    logger.info('Возвращены уникальные значения атрибута')

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
    
    logger.info('Показаны графики')

@st.cache_data
def class_prop(target: pd.Series) -> pd.DataFrame:
    '''
    Возвращает соотношение классов.
    '''
    logger.info('Возвращены соотношения классов')

    return target.value_counts(normalize=True).to_frame()


def eda():
    '''
    Результаты разведовательного анализа данных.
    '''
    st.header("EDA")

    data = upload_data('page_twitter/final.csv')
    data = data[['username',
                 'ticker',
                 'text',
                 'year',
                 'month',
                 'day',
                 '1_day_after']]

    st.write(data)
    st.write(f'''
    Для обучения модели было отобрано {data.shape[0]}
    твита инфлюенсеров из финансовой сферы по выбранным тикерам.
    Таргетом является столбец 1_day_after,
    т.е. вырастет цена акции на следующий день
    после публикации твита или нет.
             ''')
    st.write("Список инфлюенсеров:")
    st.write(get_unique(data['username']))
    st.write("Список тикеров:")
    st.write(get_unique(data['ticker']))

    show_images()

    st.write('Соотношение классов:')
    st.write(class_prop(data['1_day_after']))

    logger.info('Вызван EDA')


@st.cache_data
def get_params():
    '''
    Получает параметры модели.
    '''
    api_url = 'http://service_twitter:8004/hyperparameters'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        logger.info('Получены параметры')
        return response.json()['hyperparameters']
    except requests.exceptions.RequestException as e:
        st.error(f"Не удалось подключиться к сервису: {e}")
        logger.error(f"Не удалось получить параметры: {str(e)}")
        return {}


def model_params():
    '''
    Параметры и гиперпараметры модели.
    '''
    st.image('eda_twitter/roc_curve.png', caption='График ROC кривой')
    params = get_params()
    if params:
        param_df = pd.DataFrame(list(params.items()),
                                columns=["Параметр", "Значение"])

        st.table(param_df)
    
    logger.info('Возвращены параметры')


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
    placeholder_text = 'The chance of $MSFT winning an appeal is slim.'
    user_input = st.text_input('Введите текст:',
                               placeholder=placeholder_text)
    if user_input:
        pred = get_predict(user_input)
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
