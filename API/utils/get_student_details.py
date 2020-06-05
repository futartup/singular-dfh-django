from student_path.student_active_paths.models import StudentActivePaths
from student_path.student_active_paths.serializers import StudentActivePathsSerializer
from student_news_feed.student_news_feed.models import StudentNewsFeed
import requests, os, json

def get_student_institute_details(res):
    try:
        colleges_of_intrest_url = os.environ['SRM_DOMAIN_NAME'] + '/api/gps/institute/?student_register=true&institute_uuid={}'.format(','.join(res['institution_uuid']))
        res_colleges_of_intrest = requests.get(colleges_of_intrest_url)
        if res_colleges_of_intrest.status_code == requests.codes.ok:
                res_colleges_of_intrest_json = res_colleges_of_intrest.json()
                res['colleges_of_intrest'] = res_colleges_of_intrest_json
        else:
            raise Exception("{} returned a status code: {}".format(colleges_of_intrest_url, res_colleges_of_intrest.status_code))
    except Exception as e:
        res['colleges_of_intrest'] = res['institution_uuid']
        print("Exception in fetching the colleges_of_intrest_url: {} Exception: {}".format(colleges_of_intrest_url, e.__str__()))
    return res

def get_student_details(request, student_uuid, res, *args, **kwargs):
    try:
        student_active_path_obj = StudentActivePaths.objects.filter(student_uuid=student_uuid, path_status=True)
        active_path_data = StudentActivePathsSerializer(instance=student_active_path_obj, many=True).data
        res['active_path'] = active_path_data
    except Exception as e:
        res['active_path'] = []
        print("Exception in fetching active_path Exception: {}".format(e.__str__()))
    
    try:
        res['news_feed'] = [obj.to_json() for obj in StudentNewsFeed.objects.filter(student_uuid=student_uuid)]
    except Exception as e:
        print("Exception in fetching news_feed Exception: {}".format(e.__str__()))
        res['news_feed'] = []

    if bool(res["institution_uuid"]):
        res = get_student_institute_details(res)
    else:
        res['colleges_of_intrest'] = []
    
    
    try:
        post_url_path  = os.environ['SRM_DOMAIN_NAME'] + '/api/gps/course-map/'
        # print(post_url_path)
        if bool(active_path_data) and 'path-info' not in kwargs:
            try:
                headers = {'Authorization': 'Bearer ' + request.META.get('HTTP_AUTHORIZATION').split(' ')[1]}
            except:
                res['path_details'] = {"path_info": {}}
                path_url_single = os.environ['SRM_DOMAIN_NAME'] + '/api/gps/publish-v1/{0}'.format(
                    active_path_data[0]['path_uuid'].__str__())
                result = requests.get(path_url_single)
                print(result.url)
                if result.status_code == requests.codes.ok:
                    res['path_details']['path_info'] = result.json()
                else:
                    res['path_details']['path_info'] = {}
                return res
            params = {'s_uuid': student_uuid,
                      'p_uuid': active_path_data[0]['path_uuid'].__str__()}
            res_account = requests.get(post_url_path, headers=headers, params=params)
            if res_account.status_code == requests.codes.ok:
                res_account_json = res_account.json()
                res['path_details'] = res_account_json
                if res_account_json['path_info']['institute_details']['name']:
                    res['my_school']=res_account_json['path_info']['institute_details']['name']
            else:
                print(res_account.content)
                raise Exception("{} returned a status code: {}".format(post_url_path, res_account.status_code))
        else:
            raise Exception("{} has no active path".format(student_uuid))
    except Exception as e:
        res['path_details'] = [{'error': e.__str__()}]
        res['my_school']= 'unenrolled'
        print("Exception in fetching the url: {} Exception: {}".format(post_url_path, e.__str__()))
        
    return res