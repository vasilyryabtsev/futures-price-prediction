from fastapi import FastAPI

app = FastAPI()

@app.get("/10_k")
async def server1_endpoint():
    return {"message": "Hello from 10_k!"}