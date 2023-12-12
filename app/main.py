from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api import api
from mangum import Mangum
import json
from utils.config import get_env_variable, configure_logging


app = FastAPI(
    title="AI Generative Services API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_env_variable("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)
logger = configure_logging()


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """
    Exception handler for handling unhandled exceptions in the API.

    Args:
        request (Request): The incoming request.
        exc (Exception): The unhandled exception.

    Returns:
        JSONResponse: The JSON response with an error message and status code 500.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


def get_asgi_handler(stage: str | None):
    """
    Get the ASGI handler for the API.

    Args:
        stage (str | None): The stage of the API.

    Returns:
        Mangum: The Mangum ASGI handler.
    """
    root_path = get_env_variable("ROOT_PATH", "ai-gen")
    app.root_path = f"/{stage}/{root_path}" if stage else f"/{root_path}"
    return Mangum(app, api_gateway_base_path=app.root_path)


def get_stage(event):
    """
    Get the deployment stage of the API from the event data.

    Args:
        event: The event data.

    Returns:
        str | None: The stage of the API.
    """
    stage_variables = event.get("stageVariables", {})
    return stage_variables.get("Stage", None) if stage_variables else None


def handler(event, context):
    """
    Lambda handler function for the API.

    Args:
        event: The event data.
        context: The context data.

    Returns:
        dict: The response from the ASGI handler.
    """
    stage = get_stage(event)
    asgi_handler = get_asgi_handler(stage)
    try:
        response = asgi_handler(event, context)
        log_data = {
            "stage": stage,
            "statusCode": response.get("statusCode", None),
            "root_path": app.root_path,
            "response": response,
            "event": event,
        }
        if response.get("statusCode") >= 400:
            logger.error(json.dumps(log_data))
        else:
            logger.info(json.dumps(log_data))
        return response
    except Exception as e:
        logger.exception("Error processing request.")
        raise
