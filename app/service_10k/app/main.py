import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytz

from app.service_10k.app import entities
from app.service_10k.app import config
from app.service_10k.app import service

logging.basicConfig(level=config.LOGGING_LEVEL)
moscow_tz = pytz.timezone('Europe/Moscow')


def moscow_time(*args, **kwargs):
    '''
    Возвращает время по Москве.
    '''
    utc_now = datetime.now(pytz.utc)
    moscow_time = utc_now.astimezone(moscow_tz)
    return moscow_time.strftime('%m.%d.%Y %H:%M:%S')


# Устанавливаем нашу функцию для формата времени
file_log = logging.FileHandler('logs/Log.log')
console_out = logging.StreamHandler()
formatter = logging.Formatter('[service_10k | %(asctime)s | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
formatter.formatTime = moscow_time
file_log.setFormatter(formatter)
console_out.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(config.LOGGING_LEVEL)
logger.addHandler(file_log)
logger.addHandler(console_out)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Loading models ans creating context
    """
    logger.info("Старт создания контекста")
    try:
        service.model_context.load_models()
        logger.info("Модели загружены")
        yield
    except Exception as e:
        logger.error("Ошибка при загрузке контекста: %s", e)
    finally:
        service.model_context.model_lr = None
        service.model_context.tokenizer = None
        service.model_context.model_bert = None

app = FastAPI(lifespan=lifespan)


@app.post("/report_prediction")
async def predict_test(file: UploadFile = File(...)) -> entities.PredictResponse:
    """
    Predicting probabilities
    """
    try:
        logger.info("Файл получен: %s", file.filename)
        contents = await file.read()
        report = contents.decode("utf-8")
        logger.info("Файл получен: %s", file.filename)
        return service.predict_text(report)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# uvicorn app.service_10k.app.main:app --reload
