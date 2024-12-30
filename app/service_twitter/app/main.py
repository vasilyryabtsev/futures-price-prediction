from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import pickle
import pandas as pd

# Инициализация приложения
app = FastAPI()

# Загрузка модели
try:
    with open("model", "rb") as input_file:
        model = pickle.load(input_file)
except FileNotFoundError:
    raise RuntimeError("Файл модели 'model' не найден")

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
        print(f"Получен запрос от клиента: {request.client}")

        # Создаем DataFrame
        df = pd.DataFrame({"text": [input_data.text]})
        print(f"Создан DataFrame: {df}")

        # Получение предсказаний и вероятностей
        probabilities = model.predict_proba(df)[0].tolist()
        print(f"Предсказания модели: {prediction}, вероятности: {probabilities}")

        # Формируем ответ
        return PredictionResponse(
            negative_probability=probabilities[0],
            positive_probability=probabilities[1]
        )
    except Exception as e:
        print(f"Ошибка в обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")

@app.get("/hyperparameters", response_model=HyperparametersResponse)
async def get_hyperparameters():
    """
    Возвращает гиперпараметры модели.
    """
    try:
        # Проверяем, поддерживает ли модель метод `get_params`
        if hasattr(model, "get_params"):
            hyperparameters = model.get_params()
            print(f"Гиперпараметры модели: {hyperparameters}")
            return HyperparametersResponse(hyperparameters=hyperparameters)
        else:
            raise HTTPException(status_code=400, detail="Модель не поддерживает метод get_params")
    except Exception as e:
        print(f"Ошибка при получении гиперпараметров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении гиперпараметров: {str(e)}")
