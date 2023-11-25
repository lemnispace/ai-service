from fastapi import FastAPI, HTTPException
from app.image_gen.image_generator import generate_image_from_text
from app.image_gen.types import GenTextToImageRequest

app = FastAPI()


@app.post("/text-to-image")
async def text_to_image(request: GenTextToImageRequest):
    try:
        return await generate_image_from_text(request)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
