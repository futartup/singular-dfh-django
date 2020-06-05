import jwt
import yaml
from API.utils.aws.add_user import check_if_group_exists, add_user_to_group

def GetUserTokenDetails(user_token):
    decoded_token = jwt.decode(user_token['access'], None, None) 
    
    if 'custom:user_portal' in decoded_token and decoded_token['custom:user_portal'].lower() == 'gps'\
        and 'custom:UserType' in decoded_token and decoded_token['custom:UserType'].lower() == 'student':
        # assign the users to the groups of college of interest if they are not assigned to
        # import pdb; pdb.set_trace()
        if 'custom:institution_uuid' in decoded_token:
            groups = []
            if 'cognito:groups' in decoded_token:
                groups = decoded_token['cognito:groups']
            institution_uuids = yaml.load(decoded_token['custom:institution_uuid'])
            if groups.__len__() < institution_uuids.__len__():
                print("need to assign the student to the college of interest group")
                for institution_uuid in institution_uuids:
                    group_name = "institute_uuid_school_of_interest_students_{}".format(institution_uuid.__str__())
                    api_check_group, _ = check_if_group_exists(group_name)
                    if api_check_group:
                        _, _ = add_user_to_group({'Username':  decoded_token['cognito:username']}, group_name)


        return True,  {
            'access': user_token['access'], 'refresh': user_token['refresh'] if 'refresh' in user_token else '',
            'srm_user': decoded_token['cognito:username']
        }
        # return {'status': 'success',}, status=status.HTTP_200_OK, safe=False
    else:
        return False, {
            'reason': "User not Found"
        }
        # return {'status': 'Failed', 'reason': "User not Found"}, status=status.HTTP_401_UNAUTHORIZED, safe=False            