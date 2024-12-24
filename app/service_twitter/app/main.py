from fastapi import FastAPI
import pickle
import pandas as pd
from FinBert import finbert, preprocessing
import transformers
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import FunctionTransformer
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import pandas as pd

app = FastAPI()

with open('model', 'rb') as input_file:
    model = pickle.load(input_file)

@app.get("/twitter")
async def server1_endpoint():
    ans = model.predict(pd.DataFrame(data={'text': ['BUY $APPL']}))
    return {"message": ans}