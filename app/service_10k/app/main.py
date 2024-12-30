import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

import entities
import service
import config


logger = logging.getLogger('uvicorn.error')


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
    

@app.get("/get_params")
async def get_params() -> entities.ParamsEntity:
    return service.get_params()


if __name__ == '__main__':
    uvicorn.run(app, log_config=config.LOGGING_CONFIG, host='0.0.0.0', port=8001)