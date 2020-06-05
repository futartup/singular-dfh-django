import hmac
import hashlib
import base64
import yaml
import os
from django.core.cache import cache

from . import USER_POOL_ID, CLIENT, CLIENT_ID, CLIENT_SECRET




def serialize_data(users):
    user_modified = []
    for user in users:
        user_details = {}
        # import pdb;pdb.set_trace()
        user_details["created_on"] = user['UserCreateDate']
        user_details["modified_on"] = user['UserLastModifiedDate']
        user_details["Enabled"] = user['Enabled']
        # user_details["is_active"] = user['Enabled']
        # user_details["is_verfied"] = True if user['UserStatus'] == 'CONFIRMED' else False
        user_details["Username"] = user['Username']
        user_details["uuid"] = user['Username']
        # user_details['notes'] = None
        # user_details['Enabled'] = user['']
        if 'Attributes' in user:
            key = 'Attributes'
        else:
            key = 'UserAttributes'
        for attribute in user[key]:
            
            if attribute['Name'] == 'given_name':
                user_details['first_name'] = attribute['Value']
            elif attribute['Name'] == 'middle_name':
                user_details['middle_name'] = attribute['Value']
            elif attribute['Name'] == 'family_name':
                user_details['last_name'] = attribute['Value']
            elif attribute['Name'] == 'custom:ethnicity':
                user_details['ethnicity'] = attribute['Value']
            elif attribute['Name'] == 'custom:citizenship':
                user_details['citizenship'] = attribute['Value']
            elif attribute['Name'] == 'custom:native_language':
                user_details['native_language'] = attribute['Value']

            elif attribute['Name'] == 'custom:facebook_link':
                user_details['facebook_link'] = attribute['Value']
            elif attribute['Name'] == 'custom:linkedin_link':
                user_details['linkedin_link'] = attribute['Value']
            elif attribute['Name'] == 'custom:twitter_link':
                user_details['twitter_link'] = attribute['Value']
            elif attribute['Name'] == 'custom:instagram':
                user_details['instagram_link'] = attribute['Value']
            elif attribute['Name'] == 'custom:bio':
                user_details['bio'] = attribute['Value']
            elif attribute['Name'] == 'custom:alternate_email':
                user_details['alternate_email'] = attribute['Value']
            
            elif attribute['Name'] == 'email':
                user_details['email'] = attribute['Value']
            elif attribute['Name'] == 'custom:institution_id':
                user_details['institution_id'] = attribute['Value']
            elif attribute['Name'] == 'custom:institution_uuid':
                user_details['institution_uuid'] = yaml.load(attribute['Value']) if attribute['Value'] else ''
            elif attribute['Name'] == 'phone_number':
                user_details['phone_number'] = attribute['Value']

            elif attribute['Name'] == 'gender':
                user_details['gender'] = attribute['Value']
            elif attribute['Name'] == 'birthdate':
                user_details['dob'] = attribute['Value']
            elif attribute['Name'] == 'custom:interest':
                user_details['interest'] = attribute['Value']

            elif attribute['Name'] == 'picture':
                user_details['photo'] = "{}{}".format(os.environ['S3_BASE_URL'],  attribute['Value'])
            elif attribute['Name'] == 'custom:banner':
                user_details['banner'] = "{}{}".format(os.environ['S3_BASE_URL'], attribute['Value'])
            elif attribute['Name'] == 'custom:resume':
                user_details['resume'] = attribute['Value']
            elif attribute['Name'] == 'address':
                user_details['address'] = yaml.load(attribute['Value'])
            elif attribute['Name'] == 'custom:student_type':
                user_details['student_type'] = attribute['Value']
            elif attribute['Name'] == 'custom:userType':
                user_details['user_type'] = attribute['Value']
            elif attribute['Name'] == 'custom:user_portal':
                user_details['user_portal'] = attribute['Value']
            elif attribute['Name'] == 'custom:institution_id':
                user_details['institute_id'] = attribute['Value']
            elif attribute['Name'] == 'custom:college_name':
                user_details['college_name'] = attribute['Value']
            
                
                
            
    # custom:student_type
    # custom:native_language
    # cebook_link
    # custom:linkedin_link
    # custom:twitter_link
    # custom:bio
    # custom:interest
    # custom:alternate_email

        user_modified.append(user_details)
    return user_modified

def get_user_detail(username):
    print('call get_user_detail in get_user_detail username {}'.format(username))
    response = CLIENT.admin_get_user(
        UserPoolId=USER_POOL_ID,
        Username=username
    )
    # import pdb;pdb.set_trace()
    user_found =[]
    user_found.append(response)
    user_serialized = serialize_data(user_found)
    return user_serialized

def get_users(username):
    cache_key = 'gps_student_details_student_uuid_{}'.format(username)
    print('call get_user_detail in get_users username {}'.format(username))
    cache_value = cache.ttl(cache_key)
    if cache_value:
        print('call get_user_detail in get_users username {} from cache'.format(username))
        res = cache.get(cache_key)
        return res
    else:
        print('call get_user_detail in get_users username {} not from cache'.format(username))
        response = CLIENT.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=username
        )
        return_serialized = serialize_data([response])
        cache.set(cache_key, return_serialized[0], timeout = 300)
        return return_serialized[0]

def get_institute_users(institution_id):
    group_name = "".join(['institute_id_', institution_id,'_students'])
    try:
        # cache_key = "_{}".format(group_name)
        # cached_value = cache.ttl(cache_key)
        # if  cached_value:
        #     resp = cache.get(cache_key)
        # else:
        resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name)
        print('call list_users_in_group in get_users Group Name {}'.format(group_name))
        # cache.set(cache_key, resp, timeout = 120)
        if resp:
            
            user_serialized = serialize_data(resp['Users'])
            return True, user_serialized
    except Exception as e:
        return False, "{}".format(str(e))

def get_users_from_group(group_name):
    def get_user(group_name, token=False):
        try:
            if token:
                resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name, NextToken=token)
            else:
                resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name)
                
            if resp:
                # user_serialized = serialize_data(resp['Users'])
                return True, resp
        except Exception as e:
            return False, "{}".format(str(e))
    final_result = []
    data = {}
    while True:
        # print('NextToken', data.get("NextToken", False))
        status_api, data = get_user(group_name, data.get("NextToken", False))
        if status_api:
            final_result.extend(data['Users'])
        if 'NextToken' not in data:
            break
    
    user_serialized = serialize_data(final_result)
    return True, user_serialized
        
    #     print('call list_users_in_group in get_users Group Name {}'.format(group_name))
    #     # cache.set(cache_key, resp, timeout = 120)
    #     if resp:
            
    #         user_serialized = serialize_data(resp['Users'])
    #         return True, user_serialized
    # except Exception as e:
    #     return False, "{}".format(str(e))

def get_users_group(institution_id):
        group_name = 'institute_id_{}_students'.format(institution_id)
        print('call list_users_in_group in get_users NO CACHE Group Name {}'.format(group_name))
        def get_user(group_name, token=False):
            try:
                if token:
                    resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name, NextToken=token)
                else:
                    resp = CLIENT.list_users_in_group(UserPoolId=USER_POOL_ID, GroupName=group_name)
                
                if resp:
                    # user_serialized = serialize_data(resp['Users'])
                    return True, resp
            except Exception as e:
                return False, "{}".format(str(e))
        final_result = []
        data = {}
        while True:
            print('NextToken', data.get("NextToken", False))
            _, data = get_user(group_name, data.get("NextToken", False))
            final_result.extend(data['Users'])
            
            if 'NextToken' not in data:
                break
        
        user_serialized = serialize_data(final_result)
        return True, user_serialized
