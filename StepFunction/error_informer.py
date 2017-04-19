__author__ = 'Heisenberg'
import requests


def _make_api_call(url, json=None):
    response = requests.post(url, json=json)
    response.raise_for_status()
    return response


def format_response(req):
    return {
        'text': 'Oh, boy!',
        'attachments': [
            {
                'text': 'Something broke, please try again',
                'image_url': 'https://media.giphy.com/media/26uf6qaxqHpYXgjWU/giphy.gif'
            }
        ]
    }


def lambda_handler(event, context):
    fmt_resp = format_response(event)
    _make_api_call(event['response_url'], json=fmt_resp)
