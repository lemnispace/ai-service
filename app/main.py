from fastapi import FastAPI
from api.api_v1 import api as api_v1
from mangum import Mangum

app = FastAPI()
app.include_router(api_v1.router, prefix="/api/v1")

handler = Mangum(app)
