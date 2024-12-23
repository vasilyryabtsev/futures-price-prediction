from fastapi import FastAPI

app = FastAPI()

@app.get("/reddit")
async def server1_endpoint():
    return {"message": "Hello from reddit!"}