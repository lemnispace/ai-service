from fastapi import FastAPI
from app.api import api
from mangum import Mangum

app = FastAPI()
app.include_router(api.router)

handler = Mangum(app)
