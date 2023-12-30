import pytest
import os
from botocore.exceptions import ClientError
from app.utils.config import get_secret, get_env_variable, get_parameter_store_client
from moto import mock_ssm
import boto3


@pytest.fixture()
def mock_ssm_env():
    with mock_ssm():
        ssm_client = boto3.client("ssm", "us-east-1")
        ssm_client.put_parameter(
            Name="api_key_name", Value="abcdef123", Type="SecureString"
        )
        yield ssm_client


def test_get_secret_valid_secret(mock_ssm_env):
    secret_name = "api_key_name"
    secret_value = "abcdef123"
    result = get_secret(mock_ssm_env, secret_name)
    assert result == secret_value


def test_get_secret_invalid_secret_name(mock_ssm_env):
    secret_name = "non_existent_secret"
    # test that an error is raised when the secret name is invalid
    with pytest.raises(ClientError):
        get_secret(mock_ssm_env, secret_name)


def test_get_parameter_store_client(mock_ssm_env):
    os.environ["AWS_PARAMETER_STORE_REGION_NAME"] = "us-west-2"
    result = get_parameter_store_client()
    assert result is not None


def test_get_parameter_store_client_with_error(mock_ssm_env):
    os.environ.pop("AWS_PARAMETER_STORE_REGION_NAME")
    with pytest.raises(ValueError):
        get_parameter_store_client()


def test_get_env_variable_existing_variable():
    env_variable_name = "TEST_VARIABLE"
    expected_value = "test_value"
    os.environ[env_variable_name] = expected_value

    result = get_env_variable(env_variable_name)
    assert result == expected_value


def test_get_env_variable_non_existing_variable():
    env_variable_name = "NON_EXISTING_VARIABLE"
    default_value = "default_value"

    result = get_env_variable(env_variable_name, default_value)
    assert result == default_value
