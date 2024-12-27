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
    text: str
    prediction: int
    probabilities: list[float]

@app.post("/twitter", response_model=PredictionResponse)
async def predict_sentiment(request: Request, response: Response, input_data: TextInput):
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
        prediction = model.predict(df)[0]
        probabilities = model.predict_proba(df)[0].tolist()
        print(f"Предсказания модели: {prediction}, вероятности: {probabilities}")

        # Формируем ответ
        response.headers["X-Custom-Header"] = "Custom Response Header Example"
        return PredictionResponse(
            text=input_data.text,
            prediction=int(prediction),
            probabilities=probabilities,
        )
    except Exception as e:
        print(f"Ошибка в обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")