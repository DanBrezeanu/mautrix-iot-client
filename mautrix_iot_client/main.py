from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from mautrix_iot_client.routers import api

app = FastAPI()
app.include_router(api.router)
