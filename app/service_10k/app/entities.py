from pydantic import BaseModel, Field


class PredictResponse(BaseModel):
    negative_probability: float
    positive_probability: float


class ParamsEntity(BaseModel):
    distilbert_tokenizer_type: str = Field("DistilBertTokenizer")
    distilbert_pretrained_model: str = Field("distilbert-base-uncased")
    distilbert_max_length: int = Field(512)
    distilbert_padding: str = Field("max_length")
    distilbert_truncation: bool = Field(True)

    logistic_regression_type: str = Field("LogisticRegression")
    logistic_regression_max_iter: int = Field(1000)
    logistic_regression_solver: str = Field("lbfgs")
    logistic_regression_multi_class: str = Field("auto")

    test_size: float = Field(0.25)
    random_state: int = Field(42)

    batch_size: int = Field(80)
    drop_na: bool = Field(True)
    start_index: int = Field(42080)
    end_index: int = Field(47080)

    train_accuracy: bool = Field(True)
    test_accuracy: bool = Field(True)
