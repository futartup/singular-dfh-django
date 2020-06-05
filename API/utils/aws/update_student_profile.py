from . import CLIENT, CLIENT_ID, CLIENT_SECRET, USER_POOL_ID


def update_student_profile(username, attributes):
    try:
        resp = CLIENT.admin_update_user_attributes(
            UserPoolId=USER_POOL_ID,
            Username=username,
            UserAttributes=attributes,
            )
        
    except CLIENT.exceptions.NotAuthorizedException as e:
        return False, "The username or password is incorrect"
    except Exception as e:
        return False, "Error: {}".format(str(e))
    return True, resp
