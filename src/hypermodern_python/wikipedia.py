import click
import requests

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


def random_page(language: str = "en"):
    url = API_URL.format(language=language)

    try:
        with requests.get(url) as response:
            requests.Response
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        raise click.ClickException(str(error)) from error
