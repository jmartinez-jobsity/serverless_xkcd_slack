__author__ = 'Heisenberg'
import random
import requests


def _make_api_call(url):
    response = requests.post(url)
    response.raise_for_status()
    return response.json()


def lambda_handler(event, context):
    url = "http://xkcd.com/info.0.json"
    response = requests.post(url)
    response.raise_for_status()
    resp = response.json()

    rand_max = resp['num']
    return random.randrange(1, rand_max)
