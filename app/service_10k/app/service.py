import logging
import torch
import pickle
import numpy as np
from transformers import AutoModel, AutoTokenizer

import entities
import config


class ModelContext:
    def __init__(self):
        """
        Initialization of context
        """
        self.loaded_gbm = None
        self.loaded_pca = None
        self.tokenizer = None
        self.model_bert = None
        self.model_path = config.PATH_MODEL
        self.model_name = config.MODEL_NAME
        self.device = torch.device(config.DEVICE)

    def load_models(self) -> None:
        """
        Loading model context
        """
        with open(self.model_path, 'rb') as file:
            self.loaded_gbm, self.loaded_pca = pickle.load(file)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model_bert = AutoModel.from_pretrained(self.model_name)
        self.model_bert = self.model_bert.to(self.device)

    def get_tokens(self, report: str):
        """
        Get tokens
        """
        return self.tokenizer(
            report[1500:6500],
            return_tensors='pt',
            max_length=512,
            padding='max_length',
            truncation=True
        ).to(self.device)
    
    def get_text_embedding(self, inputs) -> np.array:
        """
        Get embeddings
        """
        outputs = self.model_bert(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
        return np.array([embeddings.detach().cpu().numpy()[0]])


model_context = ModelContext()
logger = logging.getLogger('uvicorn.error')


def predict_text(report: str) -> entities.PredictResponse:
    """
    This method involves tokenization and vectorization of
    text, as well as forecasting
    """
    logger.info('Токенизация начата')
    inputs = model_context.get_tokens(report)
    logger.info('Токенизация завершена')
    
    logger.info('Старт расчета эмбеддингов')
    vectors = model_context.get_text_embedding(inputs)
    logger.info('Расчет эмбеддингов завершен')
    
    logger.info('Снижение размерности эмбеддингов')
    vectors_pca = model_context.loaded_pca.transform(vectors)
    logger.info('Размерность эмбеддингов снижена')
    
    logger.info('Старт прогнозирования вероятности')
    probs = model_context.loaded_gbm.predict(
        data=vectors_pca, 
        num_iteration=model_context.loaded_gbm.best_iteration
    )
    logger.info('Прогнозирование вероятности завершено')
    
    prob_pos = probs[0]
    prob_neg = 1 - prob_pos
    response = entities.PredictResponse(
        negative_probability=prob_neg,
        positive_probability=prob_pos
    )

    return response


def get_parameters() -> entities.ParamsEntity:
    """
    Return an instance of ParamsEntity with default parameters.
    """
    logger.info('Запрошена информация о гиперпараметрах обучения')
    return entities.ParamsEntity(
        pca_params=model_context.loaded_pca.get_params(),
        gbm_params=model_context.loaded_gbm.params
    )
