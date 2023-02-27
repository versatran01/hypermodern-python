import click.testing
from click.testing import CliRunner as Runner
import pytest
import requests

from hypermodern_python import console

# def test_main_succeeds():
#     runner = click.testing.CliRunner()
#     result = runner.invoke(console.main)
#     assert result.exit_code == 0


@pytest.fixture
def mock_requests_get(mocker):
    # Use mocker.patch to replace the requests.get function with a mock.
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Mock title",
        "extract": "Mock extract",
    }
    return mock


@pytest.fixture
def runner() -> Runner:
    return Runner()


def test_main_succeeds(runner: Runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: Runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Mock title" in result.output


def test_main_invokes_requests_get(runner: Runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: Runner, mock_requests_get):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(runner: Runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(runner: Runner,
                                              mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output