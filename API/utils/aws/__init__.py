"""
Refer this document for more API's :
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.sign_up
"""


import boto3
import os

USER_POOL_ID = os.environ["AWS_COGNITO_USER_POOL_ID"]
CLIENT_ID = os.environ["AWS_COGNITO_CLIENT_ID"]
CLIENT_SECRET = os.environ["AWS_COGNITO_CLIENT_SECRET"]
CLIENT = boto3.client('cognito-idp')