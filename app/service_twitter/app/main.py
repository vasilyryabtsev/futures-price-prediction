from fastapi import FastAPI

app = FastAPI()

@app.get("/twitter")
async def server1_endpoint():
    return {"message": "Hello from twitter!"}