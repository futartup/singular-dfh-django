
from . import CLIENT, CLIENT_ID, CLIENT_SECRET, USER_POOL_ID


def check_student_profile(token, attribute_name, code):
    resp = CLIENT.verify_user_attribute(
        #UserPoolId=USER_POOL_ID,
        AccessToken=token,
        AttributeName=attribute_name,
        Code=code
    )
    return resp