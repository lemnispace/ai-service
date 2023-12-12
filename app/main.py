from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api
from mangum import Mangum

app = FastAPI(
    title="AI Generative Services API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/ai-gen")


def handler(event, context):
    stage_variables = event.get("stageVariables", {})
    stage = stage_variables.get("Stage", "") if stage_variables else ""
    if stage:
        app.root_path = f"/{stage}"
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response
