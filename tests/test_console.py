from unittest.mock import Mock

from click.testing import CliRunner as Runner
import pytest
from pytest_mock import MockFixture
import requests

from hypermodern_python import console
from hypermodern_python import wikipedia

# def test_main_succeeds():
#     runner = click.testing.CliRunner()
#     result = runner.invoke(console.main)
#     assert result.exit_code == 0


@pytest.fixture
def runner() -> Runner:
    return Runner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    return mocker.patch("hypermodern_python.wikipedia.random_page")


def test_main_succeeds(runner: Runner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: Runner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert "Mock title" in result.output


def test_main_invokes_requests_get(runner: Runner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: Runner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(runner: Runner, mock_requests_get: Mock) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: Runner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_random_page_uses_given_language(mock_requests_get: Mock) -> None:
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]


def test_main_uses_specified_language(
    runner: Runner, mock_wikipedia_random_page: Mock
) -> None:
    language = "pl"
    runner.invoke(console.main, [f"--language={language}"])
    mock_wikipedia_random_page.assert_called_with(language=language)


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: Runner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
