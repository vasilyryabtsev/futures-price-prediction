from fastapi import FastAPI

app = FastAPI()


@app.get("/reddit")
async def server1_endpoint():
    '''
    Возвращает ответ от сервера.
    '''
    return {"message": "Hello from reddit!"}
