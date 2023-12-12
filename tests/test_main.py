from app.main import handler, app

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
    "path": "/ai-gen/docs",
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
        "path": "/Stage/ai-gen/{docs}",
        "protocol": "HTTP/1.1",
        "requestId": "bca00121aasdvsd",
        "requestTime": "12/Dec/2023:15:44:02 +0000",
        "requestTimeEpoch": 90312312311,
        "resourceId": "abc923",
        "resourcePath": "/ai-gen/{proxy+}",
        "stage": "Stage",
    },
    "resource": "/ai-gen/{proxy+}",
    "stageVariables": None,
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
    event = dict(TEST_EVENT)
    event["stageVariables"] = None
    response = handler(event, {})
    assert response["statusCode"] != 500
    assert app.root_path == "/ai-gen"
