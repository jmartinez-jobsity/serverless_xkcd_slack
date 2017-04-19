__author__ = 'Heisenberg'
import boto3
import json
import os
import random
import requests

from base64 import b64decode
from urlparse import parse_qs


ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']
kms = boto3.client('kms')
expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']


def _make_api_call(url):
    response = requests.post(url)
    response.raise_for_status()
    return response.json()


def get_comic_by_id(comic_id):
    url = "http://xkcd.com/{}/info.0.json".format(comic_id)
    return _make_api_call(url)


def get_random_comic():
    url = "http://xkcd.com/info.0.json"
    resp = _make_api_call(url)
    rand_max = resp['num']
    rand = random.randrange(1, rand_max)
    return get_comic_by_id(rand)


def format_response(resp, req):
    return {
        'response_type': 'in_channel',
        'attachments': [
            {
                'text': '{} - {}'.format(resp['num'], resp['alt']),
                'image_url': resp['img']
            }
        ]
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'], keep_blank_values=True)
    if params['token'][0] != expected_token:
        return {'statusCode': '400', 'body': 'Not Allowed'}

    try:
        if params['text'][0]:
            comic_resp = get_comic_by_id(params['text'][0])
        else:
            comic_resp = get_random_comic()
        return {'statusCode': '200',
                'body': json.dumps(format_response(comic_resp, params)),
                'headers': {
                    'Content-Type': 'application/json',
                },
        }
    except:
        return {'body': 'Something went wrong'}
