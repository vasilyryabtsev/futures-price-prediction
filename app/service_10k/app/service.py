import logging
import torch
import joblib
from transformers import DistilBertTokenizer, DistilBertModel

import entities
import config


class ModelContext:
    def __init__(self):
        """
        Initialization of context
        """
        self.model_lr = None
        self.tokenizer = None
        self.model_bert = None
        self.device = torch.device(config.DEVICE)

    def load_models(self):
        """
        Loading model context
        """
        self.model_lr = joblib.load(config.PATH_LR_MODEL)
        model_name = 'distilbert-base-uncased'
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model_bert = DistilBertModel.from_pretrained(model_name)


model_context = ModelContext()
logger = logging.getLogger('uvicorn.error')


def predict_text(report: str) -> entities.PredictResponse:
    """
    This method involves tokenization and vectorization of
    text, as well as forecasting
    """
    logger.info('Токенизация начата')
    content_device = model_context.device
    tokens = model_context.tokenizer(report[42080:47080],
                                     return_tensors='pt',
                                     padding=True,
                                     truncation=True).to(content_device)
    logger.info('Токенизация завершена')
    logger.info('Старт расчета эмбеддингов')
    with torch.no_grad():
        outputs = model_context.model_bert(**tokens)
        embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    logger.info('Расчет эмбеддингов завершен')

    logger.info('Старт прогнозирования вероятности')
    probabilities = model_context.model_lr.predict_proba(embedding)
    logger.info('Прогнозирование вероятности завершено')

    response = entities.PredictResponse(
        negative_probability=probabilities[0][0],
        positive_probability=probabilities[0][1]
    )

    return response


def get_parameters() -> entities.ParamsEntity:
    """
    Return an instance of ParamsEntity with default parameters.
    """
    logger.info('Запрошена информация о гиперпараметрах обучения')
    return entities.ParamsEntity()
