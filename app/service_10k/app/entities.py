from pydantic import BaseModel


class PredictResponse(BaseModel):
    negative_probability: float
    positive_probability: float
