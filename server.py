from fastapi import FastAPI

from app.api.webhooks import router

app = FastAPI(title="WA Status Receiver")
app.include_router(router)
