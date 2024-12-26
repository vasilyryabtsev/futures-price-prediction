from fastapi import FastAPI, File, UploadFile
import logging
from contextlib import asynccontextmanager
# import app.service_10k.app.config as config
import config as config
from fastapi.responses import JSONResponse
# import app.service_10k.app.service as service
import service
# import app.service_10k.app.entities as entities
import entities
import pytz
from datetime import datetime

# logging.basicConfig(level=config.LOGGING_LEVEL)
moscow_tz = pytz.timezone('Europe/Moscow')

# Функция для настройки времени в московской временной зоне
def moscow_time(*args, **kwargs):
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

# logger.info('Info message??))')

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Старт создания контекста")
    try:
        service.model_context.load_models() 
        logger.info("Модели загружены")
        yield 
    except Exception as e:
        logger.error(f"Ошибка при загрузке контекста: {e}")
    finally:
        service.model_context.model_lr = None
        service.model_context.tokenizer = None
        service.model_context.model_bert = None

app = FastAPI(lifespan=lifespan)

@app.get("/10_k")
async def server1_endpoint():
    return {"message": "Hello from 10_k!"}

@app.post("/report_prediction")
async def predict_test(file: UploadFile = File(...)) -> entities.PredictResponse:
    try:
        logger.info(f"Файл получен: {file.filename}")
        contents = await file.read()
        report = contents.decode("utf-8")
        logger.info(f"Файл прочитан: {file.filename}")
        return service.predict_text(report)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# uvicorn app.service_10k.app.main:app --reload