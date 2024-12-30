import logging
from contextlib import asynccontextmanager
import pickle
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd
import uvicorn
import config

logger = logging.getLogger('uvicorn.error')


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Загрузка модели
    """
    try:
        logger.info('Началась загрузка модели')
        with open("model", "rb") as input_file:
            model = pickle.load(input_file)
            app.state.model = model
        logger.info('Модель загружена')
        yield
    except FileNotFoundError as e:
        raise RuntimeError("Файл модели 'model' не найден") from e


app = FastAPI(lifespan=lifespan)


class TextInput(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    negative_probability: float
    positive_probability: float


class HyperparametersResponse(BaseModel):
    hyperparameters: dict


@app.post("/report_prediction", response_model=PredictionResponse)
async def predict_sentiment(request: Request, input_data: TextInput):
    """
    Принимает текст на вход и возвращает предсказания модели.
    """

    # Логирование запроса
    logger.info('Получен запрос от клиента: %s', request.client)

    # Создаем DataFrame
    df = pd.DataFrame({"text": [input_data.text]})
    logger.info('Создан DataFrame')

    # Получение предсказаний и вероятностей
    prediction = app.state.model.predict(df)[0]
    probabilities = app.state.model.predict_proba(df)[0].tolist()
    logger.info('Предсказание модели: %s', prediction)
    logger.info('Вероятности: %s', probabilities)

    # Формируем ответ
    return PredictionResponse(
        negative_probability=probabilities[0],
        positive_probability=probabilities[1]
    )


def filter_serializable(obj):
    '''
    Подготовка объекта к сериализации.
    '''
    if callable(obj):
        return str(obj)
    try:
        json.dumps(obj)
        return obj
    except (TypeError, OverflowError):
        return str(obj)


@app.get("/hyperparameters", response_model=HyperparametersResponse)
async def get_hyperparameters():
    """
    Возвращает гиперпараметры модели.
    """

    hyperparameters = app.state.model.get_params()
    logger.info('Гиперпараметры модели: %s', hyperparameters)
    serialized = {key: filter_serializable(value) for key,
                  value in hyperparameters.items()}
    return HyperparametersResponse(hyperparameters=serialized)


if __name__ == '__main__':
    uvicorn.run(app,
                log_config=config.LOGGING_CONFIG,
                host='0.0.0.0',
                port=8004)
