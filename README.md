
# AI-service

Integration with AI models and APIs for image/text generation deployed on AWS Lambda.

## Install

```bash
pip install -r requirements.txt
```

## Run

To run the app locally, you need to have the following environment variables set:

```bash
STABILITY_API_HOST=https://api.stability.ai
STABILITY_API_HOST_GEN=https://api.stability.ai/v1/generation
STABILITY_API_KEY=your_api_key
```

You can then run the app with the following command:

```bash
cd app # change to the app directory first
uvicorn main:app --reload
```

To invoke the Lambda function locally, you can use the following command **from the root directory** of the project:

```bash
sam local invoke AIModelFunction --event events/event.json -n env.json
```

Ensure that the `env.json` file contains the environment variables mentioned above:

```json
{
  "STABILITY_API_HOST": "https://api.stability.ai",
  "STABILITY_API_HOST_GEN": "https://api.stability.ai/v1/generation",
  "STABILITY_API_KEY": "your_api_key"
}
```

The `events/event.json` file contains example event data that you can use to test the Lambda function locally.

## Usage

Make a POST request to the `/api/v1/text-to-image` endpoint with a JSON body containing the following fields:

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

## Development with AWS SAM

If you have not configured your AWS CLI with SSO, run the following command:

```bash
aws configure sso --profile [your-profile]
```

Then run the following command to login:

```bash
aws sso login --profile [your-profile]
```

To deploy the Lambda function to AWS, you can use the following command:

```bash
sam build --profile [your-profile]
sam deploy --guided --profile [your-profile]
```

If you have already deployed the Lambda function and only want to update the function code, you can use the following command:

```bash
sam build --profile [your-profile]
sam deploy --profile [your-profile]
```
