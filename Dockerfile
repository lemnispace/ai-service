FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx unzip
# Download and install AWS SAM CLI
RUN curl -Lo aws-sam-cli-linux-arm64.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-arm64.zip
RUN unzip aws-sam-cli-linux-arm64.zip -d sam-installation
RUN ./sam-installation/install
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt
# Copy local code to the container image here to avoid re-running pip install on every code change.
COPY ./app /code/app
