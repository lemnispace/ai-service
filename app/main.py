from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api import api
from mangum import Mangum
import json
import uuid
import time
from utils.config import get_env_variable, configure_logging


app = FastAPI(
    title="AI Generative Services API",
)

# Configure CORS with security best practices
allowed_origins_str = get_env_variable("ALLOWED_ORIGINS", "")
if not allowed_origins_str:
    # For development only - in production, ALLOWED_ORIGINS must be explicitly set
    allowed_origins_str = "http://localhost:3000,http://localhost:8000"

allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# Never use allow_credentials=True with allow_origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# Request ID tracking middleware
@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    """Add request ID and timing information to all requests"""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.time()

    # Add request ID to request state
    request.state.request_id = request_id

    response = await call_next(request)

    # Add request ID and timing to response headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(time.time() - start_time)

    return response

app.include_router(api.router)
logger = configure_logging()


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring service availability.

    Returns:
        dict: Service health status
    """
    try:
        # Verify critical environment variables are set
        required_vars = ["STABILITY_API_HOST_GEN", "AWS_PARAMETER_STORE_REGION_NAME", "STABILITY_API_KEY_NAME"]
        missing_vars = [var for var in required_vars if not get_env_variable(var, None)]

        if missing_vars:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "message": f"Missing required environment variables: {', '.join(missing_vars)}"
                }
            )

        return {
            "status": "healthy",
            "service": "ai-service",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Health check failed"}
        )


@app.get("/readiness")
async def readiness_check():
    """
    Readiness check endpoint for determining if service is ready to accept traffic.

    Returns:
        dict: Service readiness status
    """
    # Could add additional checks here like database connectivity, etc.
    return {
        "status": "ready",
        "service": "ai-service"
    }


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
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"Unhandled exception (request_id: {request_id}): {exc}",
        exc_info=True,
        extra={"request_id": request_id}
    )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "request_id": request_id}
    )


def get_asgi_handler(stage: str | None):
    """
    Get the ASGI handler for the API.

    Args:
        stage (str | None): The stage of the API.

    Returns:
        Mangum: The Mangum ASGI handler.
    """
    root_path = get_env_variable("ROOT_PATH", "")
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
