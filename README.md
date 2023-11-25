
# AI-service

Integration with AI models and APIs for image/text generation.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Usage

Make a POST request to the `/text-to-image` endpoint with a JSON body containing the following fields:

```json
{
  "prompt": "portrait of a girl laughing",
  "negative_prompt": "blurry, bad",
  "seed": 681726210,
  "width": 512,
  "height": 512,
  "samples": 2
}
```
