from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from app.image_gen.image_generator import generate_image
from app.image_gen.types import GenTextToImageRequest

app = FastAPI()


@app.post("/text-to-image")
async def text_to_image(request: GenTextToImageRequest):
    try:
        return await generate_image(request)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
