from fastapi import FastAPI

app = FastAPI()


@app.get("/news")
async def server1_endpoint():
    '''
    Возвращает ответ от сервера.
    '''
    return {"message": "Hello from news!"}
