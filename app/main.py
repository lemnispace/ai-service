from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api
from mangum import Mangum

ROOT_PATH = "ai-gen"
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

app.include_router(api.router)


def handler(event, context):
    stage_variables = event.get("stageVariables", {})
    stage = stage_variables.get("Stage", None) if stage_variables else None
    app.root_path = f"/{stage}/{ROOT_PATH}" if stage else f"/{ROOT_PATH}"
    asgi_handler = Mangum(app, api_gateway_base_path=app.root_path)
    response = asgi_handler(event, context)
    return response
