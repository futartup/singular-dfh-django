from django.test import TestCase

# Create your tests here.
from django.test import TestCase
# from .views import UserTokenViewSet
from rest_framework.test import APITestCase, APIClient
from .utils.aws.get_user_token import get_user_token
import os, requests



# from API.utils.aws.add_user import AddUser
# from API.utils.aws.get_users import get_users, get_matching_user,get_user_details

# Create your tests here.


class BaseAPITestcase(APITestCase):

    token = ""
    client = APIClient()

    def get_token(self, username="ajith.sundararaj+debuggps@accionlabs.com", password="Accion@123"):
        data = {
            "username": username,
            "password": password
        }
        status_api, user_token = get_user_token(data['username'], data['password'])
        token = user_token["access"]
        return token

    def get(self,url,code = None, srm_token = None):
        if srm_token:
            self.token = srm_token
            print(self.token)
        else:
            if not self.token:
                self.token = self.get_token()
        print(self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.get(url, format='json')
        if code:
            self.assertEqual(res.status_code, code)
        else:
            self.assertEqual(res.status_code, 200)
        return res

    def post(self,url,data=None,code = None):
        if not self.token:
            self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.post(url, data= data, format='json')
        if code:
            self.assertEqual(res.status_code, code)
        else:
            self.assertEqual(res.status_code, 201)
        return res

    def put(self,url,data=None,code = None):
        if not self.token:
            self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.put(url, data= data, format='json')
        if code:
            self.assertEqual(res.status_code, code)
        else:
            self.assertEqual(res.status_code, 201)
        return res

    def patch(self,url,data=None,code = None):
        if not self.token:
            self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.patch(url, data= data, format='json')
        if code:
            self.assertEqual(res.status_code, code)
        else:
            self.assertEqual(res.status_code, 201)
        return res

    def delete(self,url,data=None,code = None):
        if not self.token:
            self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.delete(url, data= data, format='json')
        if code:
            self.assertEqual(res.status_code, code)
        else:
            self.assertEqual(res.status_code, 201)
        return res


class LoginAPITestcase(BaseAPITestcase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_get_path(self):
        res = self.get("/api/mypaths/")
        print(res.content)

    def test_post_path(self):
        data = {
            "operation": "save_path",
            "group": "sg",
            "paths": [
                {
                    "path_uuid": "466c303b-7929-4214-88b5-66daceadd925",
                    "name": "Agricultural Power Equipment Technology",
                    "attachment": "https://stargate-cdn.startmypathway.com/qa/srm/careerPath/banner/466c303b-7929-4214-88b5-66daceadd925/cyber-security.jpg"
                }
                ]
            }
        res = self.post("/api/mypaths/",data,200)
        print(res.content)


    def test_post_profile(self):

        data = {"method":"retrieve"}
        res = self.post("/api/myprofile/", data, 200)
        print(res.content)


class Utility():

    srm_token = "eyJraWQiOiJhczlHd0hVMml5MlN5T1JLeVo1MnVUVGhcLytTYUFXMGdtR01UXC95aGFRK009IiwiYWxnIjoiUlMyNTYifQ.ey" \
                    "JzdWIiOiIzMTgwYzU0OS1jNmU3LTQ5MTktODllOC1lMmY4MWVhY2RmY2YiLCJjdXN0b206aW5zdGl0dXRpb25faWQiOiIzIiwiY29nb" \
                    "ml0bzpncm91cHMiOlsiaW5zdGl0dXRlX2lkXzQ0YzkxZDFlLWI5NGQtNDViOS1hNzgxLWQ4YTliYTc5OGM5NiJdLCJlbWFpbF92ZXJpZ" \
                    "mllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfeEJhTlFsZW" \
                    "NLIiwiY3VzdG9tOnVzZXJfcG9ydGFsIjoic3JtIiwiY29nbml0bzp1c2VybmFtZSI6IjMxODBjNTQ5LWM2ZTctNDkxOS04OWU4LWUyZjgxZWFj" \
                    "ZGZjZiIsImN1c3RvbTp0ZW5hbnRfaWQiOiIzIiwiZ2l2ZW5fbmFtZSI6IkNocmlzIiwicGljdHVyZSI6Imh0dHBzOlwvXC9zdGFyZ2F0ZS1jZG4u" \
                    "c3RhcnRteXBhdGh3YXkuY29tXC9xYVwvc3JtXC8zMTgwYzU0OS1jNmU3LTQ5MTktODllOC1lMmY4MWVhY2RmY2ZcL3Byb2ZpbGUtcGljXC81ZGIxZTB" \
                    "lNGRlZTAxOTU3MjcwZmZjNzguanBnIiwiYXVkIjoibGw4dHVqNWRobDQ2ZTkxMnE1dG9hbHM0YSIsImV2ZW50X2lkIjoiODA4ZjAyYzgtOTFjOS00MDFmLTkzYz" \
                    "YtMDk0NmViOGIyYTY5IiwiY3VzdG9tOlVzZXJUeXBlIjoiQ29sbGVnZSBBZG1pbmlzdHJhdG9yIiwiY3VzdG9tOmxvZ28iOiJodHRwczpcL1wvc3RhcmdhdGUtY2RuLnN" \
                    "0YXJ0bXlwYXRod2F5LmNvbVwvcWFcL3NybVwvaW5zdGl0dXRpb25cL2xvZ29cLzQ0YzkxZDFlLWI5NGQtNDViOS1hNzgxLWQ4YTliYTc5OGM5NiIsInRva2Vu" \
                    "X3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTg3MjgxMDEyLCJwaG9uZV9udW1iZXIiOiIrMTA5ODc2NTQzMjEiLCJleHAiOjE1ODcyODQ2MTIsImlhdCI6MTU4NzI4" \
                    "MTAxMiwiZmFtaWx5X25hbWUiOiJNb3JyaXMiLCJlbWFpbCI6ImNoZXRhbi5jaGFjaGFkaSttb3JAYWNjaW9ubGFicy5jb20iLCJjdXN0b206aW5zdGl0dXRp" \
                    "b25fdXVpZCI6IjQ0YzkxZDFlLWI5NGQtNDViOS1hNzgxLWQ4YTliYTc5OGM5NiJ9.rN5QJqsa9sAS_HZs5HdadlYd84DKWyxuZ6k6BBLASgR6UougYCSxwCHfdo" \
                    "nYVQUZhNqkoXspGZ9h5WufybtuTeIPQmckar6zGYomVWXPBbQiVUAv2lIpinnBP96SDFxgm82O_3kEYZq7O1zPg01YenbHSu95ctCL3yOrZ0ipjdocsEgtpm6A8yof7" \
                    "V7AOmiTPh5sA-9KWlPQqhJgn8leqhdOYdX6gZoKkL6F_PgwUBX-D2kfoNzEfzz_cl87MsBwQtbD2QPINdAw0kQcc9TbNKeA9FI1_6lcwie7DqbI5pj1asNtj2dbuW3kq" \
                    "wCw5cM-5CJYf7HvyhQ6mt81On3dnQ"

    def get_paths(self, url):
        url = os.environ['SRM_DOMAIN_NAME'] + url

        resp = requests.get(url)
        if resp.status_code == 200:
            self.paths_list = resp.json()
            return len(resp.json()), resp.json()
        else:
            return 0, []
