import pytest


@pytest.fixture
def mock_requests_get(mocker):
    # Use mocker.patch to replace the requests.get function with a mock.
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Mock title",
        "extract": "Mock extract",
    }
    return mock


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
