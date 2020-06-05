# Singular Diffie-Helman

The code to get and submit key can be found [here](https://github.com/futartup/singular-dfh-django/blob/master/dfh/views.py)

## To get the key
```
curl -X GET \
  'http://localhost:8000/api/get-key?email=anup25111@gmail.com' \
  -H 'Postman-Token: 6bdd6299-e9d3-43c7-9caf-a980f63939aa' \
  -H 'cache-control: no-cache'
```

## To submit the key
```
curl -X GET \
  'http://localhost:8000/api/submit?email=anup25111@gmail.com&B_public=4&solution=12' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: b85a9731-4f0f-48b2-a093-b40cc32b8580' \
  -H 'cache-control: no-cache'
 ```
 
## Utility files
- [DockerFile]( https://github.com/futartup/singular-dfh-django/blob/master/Dockerfile)
- [Deployment Script](https://github.com/futartup/singular-dfh-django/blob/master/deploy.sh)
- [Jenkins File](https://github.com/futartup/singular-dfh-django/blob/master/Jenkinsfile)
