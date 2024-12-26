from fastapi import FastAPI, File, UploadFile
import logging
from contextlib import asynccontextmanager
import app.service_10k.app.config as config
from fastapi.responses import JSONResponse
import app.service_10k.app.service as service
import app.service_10k.app.entities as entities

logging.basicConfig(level=config.LOGGING_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Старт создания контекста")
    try:
        service.model_context.load_models() 
        logging.info("Модели загружены")
        yield 
    except Exception as e:
        logging.error(f"Ошибка при загрузке контекста: {e}")
    finally:
        service.model_context.model_lr = None
        service.model_context.tokenizer = None
        service.model_context.model_bert = None

app = FastAPI(lifespan=lifespan)

@app.post("/report_prediction")
async def predict_test(file: UploadFile = File(...)) -> entities.PredictResponse:
    try:
        logging.info(f"Файл получен: {file.filename}")
        contents = await file.read()
        report = contents.decode("utf-8")
        logging.info(f"Файл прочитан: {file.filename}")
        return service.predict_text(report)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# uvicorn app.service_10k.app.main:app --reload