import hmac
import hashlib
import base64

from . import CLIENT, CLIENT_ID, CLIENT_SECRET, USER_POOL_ID


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def get_user_token(username, password):
    username = username.lower()
    username = username.strip()
    try:
        resp = CLIENT.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password
            },
            ClientMetadata={
                'username': username,
                'password': password
            })
        # print(resp)
    except CLIENT.exceptions.NotAuthorizedException:
        return False, "The username or password is incorrect."
    except CLIENT.exceptions.UserNotConfirmedException:
        return False, "User is not confirmed."
    except Exception as e:
        print(e)
        return False, str(e)
    if 'AuthenticationResult' in resp:
        token = {
            'access': resp['AuthenticationResult']['IdToken'],
            'refresh': resp['AuthenticationResult']['RefreshToken'],
            'token': resp['AuthenticationResult']['AccessToken']
        }
        # id_token = resp['AuthenticationResult']['IdToken']
        return True, token
    return True, resp


def get_user_token_using_refresh_token(username, refresh_token):
    try:
        resp = CLIENT.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
                'SECRET_HASH': get_secret_hash(username)
            }
        )
    except CLIENT.exceptions.NotAuthorizedException:
        return False, "Incorrect username or password"
    except CLIENT.exceptions.UserNotFoundException:
        return False, "Username does not exists"
    except Exception as e:
        return False, str(e)
    if 'AuthenticationResult' in resp:
        token = {
            'access': resp['AuthenticationResult']['IdToken'],
            'token': resp['AuthenticationResult']['AccessToken'],
            'refresh': refresh_token
        }
        return True, token
    return True, resp
