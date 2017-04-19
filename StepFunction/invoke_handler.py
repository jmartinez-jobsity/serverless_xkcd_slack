__author__ = 'Heisenberg'
import boto3
import json
import os

from base64 import b64decode
from urlparse import parse_qs


ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']
kms = boto3.client('kms')
expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']
step_functions = boto3.client('stepfunctions')


def _unlist_params(params):
    return {k: v[0] for k, v in params.iteritems()}


def lambda_handler(event, context):
    try:
        params = _unlist_params(parse_qs(event['body'], keep_blank_values=True))
        if params['token'] != expected_token:
            return {'StatusCode': '400', 'body': 'Not Allowed'}

        step_functions.start_execution(
            stateMachineArn=os.environ['STEP_FUNC_ARN'],
            input=json.dumps(params),
        )
        return {'body': 'Your command is being processed, results will be posted in a while'}
    except:
        return {'body': 'Something went wrong'}
