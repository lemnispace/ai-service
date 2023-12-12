from app.main import handler, app

TEST_EVENT = {
    "body": None,
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Dnt": "1",
        "Host": "localhost:3000",
        "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "X-Forwarded-Port": "3000",
        "X-Forwarded-Proto": "http",
    },
    "httpMethod": "GET",
    "isBase64Encoded": False,
    "multiValueHeaders": {
        "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        ],
        "Accept-Encoding": ["gzip, deflate, br"],
        "Accept-Language": ["en-US,en;q=0.9"],
        "Cache-Control": ["max-age=0"],
        "Connection": ["keep-alive"],
        "Dnt": ["1"],
        "Host": ["localhost:3000"],
        "Sec-Ch-Ua": [
            '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
        ],
        "Sec-Ch-Ua-Mobile": ["?0"],
        "Sec-Ch-Ua-Platform": ['"macOS"'],
        "Sec-Fetch-Dest": ["document"],
        "Sec-Fetch-Mode": ["navigate"],
        "Sec-Fetch-Site": ["same-origin"],
        "Sec-Fetch-User": ["?1"],
        "Upgrade-Insecure-Requests": ["1"],
        "User-Agent": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ],
        "X-Forwarded-Port": ["3000"],
        "X-Forwarded-Proto": ["http"],
    },
    "multiValueQueryStringParameters": None,
    "path": "/ai-gen/docs",
    "pathParameters": {"proxy": "docs"},
    "queryStringParameters": None,
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "1234567890",
        "domainName": "localhost:3000",
        "extendedRequestId": None,
        "httpMethod": "GET",
        "identity": {
            "accountId": None,
            "apiKey": None,
            "caller": None,
            "cognitoAuthenticationProvider": None,
            "cognitoAuthenticationType": None,
            "cognitoIdentityPoolId": None,
            "sourceIp": "127.0.0.1",
            "user": None,
            "userAgent": "Custom User Agent String",
            "userArn": None,
        },
        "path": "/ai-gen/{proxy+}",
        "protocol": "HTTP/1.1",
        "requestId": "8348462a-d4a4-4906-bfcf-fef6d59ca1e4",
        "requestTime": "12/Dec/2023:14:57:09 +0000",
        "requestTimeEpoch": 1702393029,
        "resourceId": "123456",
        "resourcePath": "/ai-gen/{proxy+}",
        "stage": "Prod",
    },
    "resource": "/ai-gen/{proxy+}",
    "stageVariables": None,
    "version": "1.0",
}


def test_handler_with_stage():
    event = dict(TEST_EVENT)
    event["stageVariables"] = {"Stage": "Testing"}
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/Testing/ai-gen"

    event["stageVariables"] = {"Stage": "Prod"}
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/Prod/ai-gen"


def test_handler_without_stage():
    response = handler(TEST_EVENT, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/ai-gen"
