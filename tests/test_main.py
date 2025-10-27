from app.main import handler, app
import os
import pytest
from moto import mock_ssm
import boto3

TEST_EVENT = {
    "body": None,
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-ASN": "141039",
        "CloudFront-Viewer-Country": "US",
        "dnt": "1",
        "Host": "babblefa3.execute-api.us-east-1.amazonaws.com",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "None",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Via": "2.0 123459adfm32342m.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "abc123==",
        "X-Amzn-Trace-Id": "Root=1-123caabme2323",
        "X-Forwarded-For": "123.456.789.123, 321.654.987.321",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https",
    },
    "httpMethod": "GET",
    "isBase64Encoded": False,
    "multiValueHeaders": {
        "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        ],
        "Accept-Encoding": ["gzip, deflate, br"],
        "Accept-Language": ["en-US,en;q=0.9"],
        "CloudFront-Forwarded-Proto": ["https"],
        "CloudFront-Is-Desktop-Viewer": ["true"],
        "CloudFront-Is-Mobile-Viewer": ["false"],
        "CloudFront-Is-SmartTV-Viewer": ["false"],
        "CloudFront-Is-Tablet-Viewer": ["false"],
        "CloudFront-Viewer-ASN": ["111111"],
        "CloudFront-Viewer-Country": ["US"],
        "dnt": ["1"],
        "Host": ["babblefa3.execute-api.us-east-1.amazonaws.com"],
        "sec-ch-ua": [
            '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
        ],
        "sec-ch-ua-mobile": ["?0"],
        "sec-ch-ua-platform": ['"macOS"'],
        "sec-fetch-dest": ["document"],
        "sec-fetch-mode": ["navigate"],
        "sec-fetch-site": ["None"],
        "sec-fetch-user": ["?1"],
        "upgrade-insecure-requests": ["1"],
        "User-Agent": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        ],
        "Via": ["2.0 123459adfm32342m.cloudfront.net (CloudFront)"],
        "X-Amz-Cf-Id": ["abc123=="],
        "X-Amzn-Trace-Id": ["Root=1-123caabme2323"],
        "X-Forwarded-For": ["123.456.789.123, 321.654.987.321"],
        "X-Forwarded-Port": ["443"],
        "X-Forwarded-Proto": ["https"],
    },
    "multiValueQueryStringParameters": None,
    "path": "/gen/ai/docs",
    "pathParameters": {"proxy": "docs"},
    "queryStringParameters": None,
    "requestContext": {
        "accountId": "2394230439",
        "apiId": "babblefa3",
        "domainName": "babblefa3.execute-api.us-east-1.amazonaws.com",
        "domainPrefix": "babblefa3",
        "extendedRequestId": "abc9823==",
        "httpMethod": "GET",
        "identity": {
            "accessKey": None,
            "accountId": None,
            "caller": None,
            "cognitoAuthenticationProvider": None,
            "cognitoAuthenticationType": None,
            "cognitoIdentityId": None,
            "cognitoIdentityPoolId": None,
            "principalOrgId": None,
            "sourceIp": "123.456.789.123",
            "user": None,
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "userArn": None,
        },
        "path": "/Stage/gen/ai/{docs}",
        "protocol": "HTTP/1.1",
        "requestId": "bca00121aasdvsd",
        "requestTime": "12/Dec/2023:15:44:02 +0000",
        "requestTimeEpoch": 90312312311,
        "resourceId": "abc923",
        "resourcePath": "/gen/ai/{proxy+}",
        "stage": "Stage",
    },
    "resource": "/gen/ai/{proxy+}",
    "stageVariables": None,
}


@pytest.fixture(autouse=True)
def mock_ssm_env():
    with mock_ssm():
        ssm_client = boto3.client("ssm", "us-east-1")
        ssm_client.put_parameter(
            Name="api_key_name", Value="abcdef123", Type="SecureString"
        )
        yield ssm_client


@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["STABILITY_API_HOST"] = "https://test_api_host.ai"
    os.environ["STABILITY_API_HOST_GEN"] = "https://test_api_host.ai/v1/gen"
    os.environ["STABILITY_API_KEY_NAME"] = "api_key_name"
    os.environ["AWS_PARAMETER_STORE_REGION_NAME"] = "region_name"
    yield
    os.environ.pop("STABILITY_API_HOST", None)
    os.environ.pop("STABILITY_API_HOST_GEN", None)
    os.environ.pop("STABILITY_API_KEY_NAME", None)
    os.environ.pop("AWS_PARAMETER_STORE_REGION_NAME", None)


def test_handler_with_stage():
    event = dict(TEST_EVENT)
    event["stageVariables"] = {"Stage": "Testing"}
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/Testing/"

    event["stageVariables"] = {"Stage": "Prod"}
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/Prod/"


def test_handler_without_stage():
    event = dict(TEST_EVENT)
    event["stageVariables"] = None
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/"


def test_handler_with_env():
    event = dict(TEST_EVENT)
    event["stageVariables"] = {"Stage": "Testing"}
    os.environ["ROOT_PATH"] = "test"
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/Testing/test"
    del os.environ["ROOT_PATH"]


def test_health_check_endpoint():
    """Test that health check endpoint returns healthy status"""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ai-service"
    assert "version" in data


def test_readiness_check_endpoint():
    """Test that readiness check endpoint returns ready status"""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["service"] == "ai-service"


def test_request_id_middleware():
    """Test that request ID middleware adds headers"""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers
