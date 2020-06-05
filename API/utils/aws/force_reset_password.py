from . import CLIENT, CLIENT_ID, CLIENT_SECRET, USER_POOL_ID
import hmac
import hashlib
import base64


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def force_reset_password(username, new_password, session, ChallengeName='NEW_PASSWORD_REQUIRED'):
    username = username.lower()
    username = username.strip()
    try:
        res_change_password = CLIENT.admin_respond_to_auth_challenge(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            ChallengeName=ChallengeName,
            ChallengeResponses={
                'USERNAME':username,
                'NEW_PASSWORD':new_password,
                'SECRET_HASH':get_secret_hash(username)
            },
            Session=session   
        )
    except CLIENT.exceptions.NotAuthorizedException:
        return False, 'Invalid session for the user.'
    except CLIENT.exceptions.CodeMismatchException:
        return False, 'Invalid session for the user.'
    except Exception as e:
        return False, str(e)
    
    token = {
            'access': res_change_password['AuthenticationResult']['IdToken'],
            'refresh': res_change_password['AuthenticationResult']['RefreshToken'],
            'token': res_change_password['AuthenticationResult']['AccessToken']
        }
    
    return True, token