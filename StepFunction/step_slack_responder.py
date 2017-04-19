__author__ = 'Heisenberg'
import requests


def _make_api_call(url, json=None):
    response = requests.post(url, json=json)
    response.raise_for_status()
    return response


def get_comic_by_id(comic_id):
    url = "http://xkcd.com/{}/info.0.json".format(comic_id)
    return _make_api_call(url).json()


def format_response(resp, req):
    return {
        'response_type': 'in_channel',
        'user_name': req['user_name'],
        'attachments': [
            {
                'text': '{} - {}'.format(resp['num'], resp['alt']),
                'image_url': resp['img']
            }
        ]
    }


def lambda_handler(event, context):
    comic_resp = get_comic_by_id(event['text'])
    fmt_resp = format_response(comic_resp, event)
    _make_api_call(event['response_url'], json=fmt_resp)
