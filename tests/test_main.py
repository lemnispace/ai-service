import os
from dotenv import load_dotenv
from app.main import get_root_path


def test_get_root_path():
    # Test case 1: Environment variable is not set
    load_dotenv()
    os.environ["ENV"] = ""
    os.environ["SERVICE_NAME"] = "ai-gen"
    assert get_root_path() == "ai-gen"

    # Test case 2: Environment variable is set
    os.environ["ENV"] = "development"
    os.environ["SERVICE_NAME"] = "ai-service"
    expected_root_path = "development/ai-service"
    assert get_root_path() == expected_root_path

    # Test case 2: Environment variable is set
    os.environ["ENV"] = "Prod"
    os.environ["SERVICE_NAME"] = ""
    expected_root_path = "Prod"
    assert get_root_path() == expected_root_path
