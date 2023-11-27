from fastapi import FastAPI
from app.routers.text_to_image import router as text_to_image_router

app = FastAPI()
app.include_router(text_to_image_router)
