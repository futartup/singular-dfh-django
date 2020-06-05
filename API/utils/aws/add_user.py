import hmac
import hashlib
import base64

from . import CLIENT, CLIENT_ID, CLIENT_SECRET, USER_POOL_ID


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def add_user(username, institute_ids, attributes):
    username = username.lower()
    username = username.strip()
    new_user = {}
    try:
        new_user = CLIENT.admin_create_user(
                Username=username,
                UserPoolId=USER_POOL_ID,
                UserAttributes=attributes,
                DesiredDeliveryMediums=["EMAIL"]
            )
        # new_user = CLIENT.sign_up(
        #     ClientId=CLIENT_ID,
        #     SecretHash=get_secret_hash(username),
        #     Username=username,
        #     Password=password,
        #     UserAttributes=attributes
        # )
    except CLIENT.exceptions.UsernameExistsException:
        return False, "User with email {} already exists".format(username)
    # except CLIENT.exceptions.InvalidParameterException:
    #         return None, "Invalid Parameters Passed"
    except Exception as e:
        return False, "Error: {}".format(str(e))
    
    user_details = new_user['User']
    # if user_details:
    #     for institute_id in institute_ids:
    #         group_name_stripped = "institute_id_{}_students".format(institute_id.replace(" ","_"))
    #         print(group_name_stripped)
    #         # check if group exists if not then create one
    #         create_group_status, res_create_group = check_if_group_exists(group_name_stripped)
    #         if create_group_status is False:
    #             return False, res_create_group
    #         # once group is created attach user to the group
    #         add_user_to_group_status, res_add_user_to_group = add_user_to_group(user_details, group_name_stripped)
    #         if add_user_to_group_status is False:
    #             return False, res_add_user_to_group
    return True, user_details


def check_if_group_exists(group_name_stripped):
    try:
        response = CLIENT.get_group(
            GroupName=group_name_stripped,
            UserPoolId=USER_POOL_ID
        )
    except CLIENT.exceptions.ResourceNotFoundException:
        return create_group(group_name_stripped)
    except Exception as e:
        return False, "Exception in check_if_group_exists {}".format(str(e))
    return True, response


def create_group(group_name):
    try:
        resp = CLIENT.create_group(
            GroupName=group_name,
            UserPoolId=USER_POOL_ID
        )
    except Exception as e:
        return False, "Exception in create_group {}".format(str(e))
    return True, resp


def add_user_to_group(user_details, group_name):
    try:
        response = CLIENT.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=user_details['Username'],
            GroupName=group_name
        )
    except Exception as e:
        return False, "Exception in add_user_to_group {}".format(str(e))
    return True, response

def remove_user_from_group(user_details, group_name):
    try:
        response = CLIENT.admin_remove_user_from_group(
            UserPoolId=USER_POOL_ID,
            Username=user_details['Username'],
            GroupName=group_name
        )
    except Exception as e:
        return False, "Exception in remove_user_from_group {}".format(str(e))
    return True, response


