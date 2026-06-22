from fastapi import FastAPI

from app.api.webhooks import w_router

app = FastAPI(title="WA Status Receiver")
app.include_router(w_router)
