from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api
from dotenv import load_dotenv
import os
from mangum import Mangum


def get_root_path():
    load_dotenv()
    env = os.getenv("ENV", "")
    service_name = os.getenv("SERVICE_NAME", "")
    return "/".join(filter(bool, [env, service_name]))


root_path = get_root_path()
app = FastAPI(
    root_path=f"/{root_path}" if root_path else None,
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

handler = Mangum(app)
