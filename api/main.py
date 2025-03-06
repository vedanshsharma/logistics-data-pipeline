from fastapi import FastAPI
from api.routes import logistics

app = FastAPI()

app.include_router(logistics.router, prefix="/logistics")


@app.get("/")
async def root():
    return {"message": "Logistics API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
