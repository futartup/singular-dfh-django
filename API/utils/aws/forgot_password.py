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


def forgot_password(username):
    secret_hash = get_secret_hash(username)
    try:
        response = CLIENT.forgot_password(
            ClientId=CLIENT_ID,
            Username=username,
            SecretHash=secret_hash
        )
    except CLIENT.exceptions.UserNotFoundException as e:
        return False, "Email {} not found.".format(username.lower())
    except CLIENT.exceptions.NotAuthorizedException:
        return False, "Email {} not activated, Please activate the email.".format(username.lower())
    except Exception as e:
        return False, e.__str__()
    return True, response

def confirm_forgot_password(username, new_password, verification_code):
    username = username.lower()
    username = username.strip()
    secret_hash = get_secret_hash(username)
    try:
        response = CLIENT.confirm_forgot_password(
                    ClientId=CLIENT_ID,
                    SecretHash=secret_hash,
                    Username=username,
                    ConfirmationCode=verification_code,
                    Password=new_password)
    except CLIENT.exceptions.ExpiredCodeException:
        return False, "Invalid code provided, please request a new code"
    except Exception as e:
        return False, e.__str__()
    return True, response