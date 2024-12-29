from fastapi import FastAPI

app = FastAPI()

@app.get("/news")
async def server1_endpoint():
    return {"message": "Hello from news! The service is currently in progress. It will be availiable as soon as possible."}