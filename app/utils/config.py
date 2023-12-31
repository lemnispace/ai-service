import os
from dotenv import load_dotenv
import logging
import boto3

load_dotenv()


def get_aws_service_client(service_name: str, region_name: str | None = None):
    """
    Get an AWS service client.

    Args:
        service_name (str): The name of the AWS service.
        region_name (str | None, optional): The AWS region name. Defaults to None.

    Returns:
        client: The AWS service client.
    """
    return boto3.client(service_name=service_name, region_name=region_name)


def get_parameter_store_client():
    """
    Get the AWS Parameter Store client.

    Returns:
       client: The AWS Parameter Store client.

    Raises:
        ValueError: If the AWS_PARAMETER_STORE_REGION_NAME environment variable is not set.
    """
    region_name = get_env_variable("AWS_PARAMETER_STORE_REGION_NAME")
    if not region_name:
        raise ValueError(
            "AWS_PARAMETER_STORE_REGION_NAME environment variable is not set"
        )
    return get_aws_service_client("ssm", region_name)


def get_env_variable(env_variable_name: str, default_value: str = "") -> str:
    """
    Get the value of an environment variable.

    Args:
        env_variable_name (str): The name of the environment variable.
        default_value (str, optional): The default value to return if the environment variable is not set. Defaults to "".

    Returns:
        str: The value of the environment variable.
    """
    return os.getenv(env_variable_name, default_value)


def configure_logging():
    """
    Configure the logging settings.

    Returns:
        logging.Logger: The logger object.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger()
    return logger


def get_secret(client, secret_name: str, with_decryption: bool = True) -> str:
    """
    Get the value of a secret from AWS Parameter Store.

    Args:
        client (botocore.client.BaseClient): The AWS Parameter Store client.
        secret_name (str): The name of the secret.
        with_decryption (bool, optional): Whether to decrypt the secret value. Defaults to True.

    Returns:
        str: The value of the secret.

    Raises:
        botocore.exceptions.ParamValidationError: If the secret name is invalid.
        botocore.exceptions.ClientError: If the secret does not exist or if there is an error retrieving the secret.
    """
    response = client.get_parameter(Name=secret_name, WithDecryption=with_decryption)
    return response["Parameter"]["Value"]
