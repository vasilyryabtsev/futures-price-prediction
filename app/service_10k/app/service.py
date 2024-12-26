# import app.service_10k.app.entities as entities
import entities
# import app.service_10k.app.config as config
import config
import torch
import joblib
from transformers import DistilBertTokenizer, DistilBertModel
import logging

logging.basicConfig(level=config.LOGGING_LEVEL)


class ModelContext:
    def __init__(self):
        self.model_lr = None
        self.tokenizer = None
        self.model_bert = None
        self.device = torch.device(config.DEVICE)

    def load_models(self):
        self.model_lr = joblib.load(config.PATH_LR_MODEL)
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model_bert = DistilBertModel.from_pretrained('distilbert-base-uncased')

model_context = ModelContext()

def predict_text(report: str) -> entities.PredictResponse:
    logging.info('Токенизация начата')
    tokens = model_context.tokenizer(report[42080:47080], return_tensors='pt', padding=True, truncation=True).to(model_context.device)
    logging.info('Токенизация завершена')
    logging.info('Старт расчета эмбеддингов')
    with torch.no_grad():
        outputs = model_context.model_bert(**tokens)
        embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    logging.info('Расчет эмбеддингов завершен')

    logging.info('Старт прогнозирования вероятности')
    probabilities = model_context.model_lr.predict_proba(embedding)
    logging.info('Прогнозирование вероятности завершено')

    response = entities.PredictResponse(
        negative_probability=probabilities[0][0],
        positive_probability=probabilities[0][1]
    )

    return response