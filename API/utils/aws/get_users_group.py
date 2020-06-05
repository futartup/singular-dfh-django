import hmac
import hashlib
import base64
import yaml
import os
from django.core.cache import cache
from .get_users import serialize_data
from . import USER_POOL_ID, CLIENT, CLIENT_ID, CLIENT_SECRET

def get_users_group(group_name):
    
    
    def get_user_from_group(group_name, token=False):
        try:
            if token:
                resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name, NextToken=token)
            else:
                resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name)
            print('call list_users_in_group in get_users NO CACHE Group Name {}'.format(group_name))
            if resp:
                return True, resp
        except Exception as e:
            # import pdb; pdb.set_trace()
            return False, "{}".format(str(e))

    final_result = []
    data = {}
    
    while True:
        api_status, data = get_user_from_group(group_name, data.get("NextToken", False))
        if api_status and 'Users' in data:
            final_result.extend(data['Users'])
        if 'NextToken' not in data:
            break
        

    
    user_serialized = serialize_data(final_result)
    return True, user_serialized
