from pydantic import BaseModel
import config


class PredictResponse(BaseModel):
    negative_probability: float
    positive_probability: float


class ParamsEntity(BaseModel):
    pretrained_bert: str = config.MODEL_NAME
    pca_params: dict
    gbm_params: dict
