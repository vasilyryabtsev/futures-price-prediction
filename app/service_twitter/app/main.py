from fastapi import FastAPI
import pickle
import pandas as pd
from FinBert import preprocessing

app = FastAPI()

with open('model', 'rb') as input_file:
    model = pickle.load(input_file)

@app.get("/twitter")
async def server1_endpoint():
    ans = model.predict(pd.DataFrame(data={'text': ['BUY $APPL']}))
    print(ans)
    return {"message": 'Hello from service_twitter!'} 