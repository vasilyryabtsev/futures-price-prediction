from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pickle
import pandas as pd
import uvicorn
import config
import logging
import json

logger = logging.getLogger('uvicorn.error')

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    except FileNotFoundError:
        raise RuntimeError("Файл модели 'model' не найден")
    
# Инициализация приложения
app = FastAPI(lifespan=lifespan)

# Описание структуры входных данных
class TextInput(BaseModel):
    text: str

# Описание структуры выходных данных
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
    try:
        # Логирование запроса
        logger.info(f"Получен запрос от клиента: {request.client}")

        # Создаем DataFrame
        df = pd.DataFrame({"text": [input_data.text]})
        logger.info(f"Создан DataFrame: {df}")

        # Получение предсказаний и вероятностей
        prediction = app.state.model.predict(df)[0]
        probabilities = app.state.model.predict_proba(df)[0].tolist()
        logger.info(f"Предсказания модели: {prediction}, вероятности: {probabilities}")

        # Формируем ответ
        return PredictionResponse(
            negative_probability=probabilities[0],
            positive_probability=probabilities[1]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")

# Удаление несериализуемых частей
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
    try:
        hyperparameters = app.state.model.get_params()
        serialized = {key: filter_serializable(value) for key, value in hyperparameters.items()}
        logger.info(f"Гиперпараметры модели: {hyperparameters}")
        return HyperparametersResponse(hyperparameters=serialized)
    except Exception as e:
        logger.info(f"Ошибка при получении гиперпараметров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении гиперпараметров: {str(e)}")

    
if __name__ == '__main__':
    uvicorn.run(app, log_config=config.LOGGING_CONFIG, host='0.0.0.0', port=8004)