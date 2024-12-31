import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
import uvicorn

from entities import PredictResponse, ParamsEntity
from service import model_context, predict_text, get_parameters
from config import LOGGING_CONFIG


logger = logging.getLogger('uvicorn.error')


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Loading models ans creating context
    """
    logger.info("Старт создания контекста")
    model_context.load_models()
    logger.info("Модели загружены")
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/report_prediction")
async def predict_test(file: UploadFile = File(...)) -> PredictResponse:
    """
    Predicting probabilities
    """
    logger.info("Файл получен: %s", file.filename)
    contents = await file.read()
    report = contents.decode("utf-8")
    logger.info("Файл получен: %s", file.filename)
    return predict_text(report)


@app.get("/get_params")
async def get_params() -> ParamsEntity:
    '''
    Model parameters.
    '''
    return get_parameters()


if __name__ == '__main__':
    uvicorn.run(app,
                log_config=LOGGING_CONFIG,
                host='0.0.0.0',
                port=8001)
