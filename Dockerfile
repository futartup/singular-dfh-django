FROM python:3.7.3-alpine
# ENV SENDGRID_API_KEY='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' \
#     USER_EMAIL="DONOTRESPOND@stargatesrm.com"\
#     TWILIO_ACCOUNT_SID="123" TWILIO_AUTH_TOKEN="!23" TWILIO_PHONE_NUMBER="123" ROOT_PAGE_NAME="stargate-srm-dev" \
#     EMAIL_HOST='smtp.sendgrid.net'\
#     EMAIL_HOST_USER='stargateinnovations'\
#     EMAIL_HOST_PASSWORD='Star*gate1'\
#     SERVER_REQUST_METHOD_HTTP='https://' SERVER_ALLOWED_HOSTS='*' SERVER_DEBUG='True' \
#     DB_HOST='db' DB_USERNAME='root' DB_PASS='password' DB_NAME='srm_backend' \
#     AWS_DEFAULT_REGION='us-east-1' \
#     AWS_ACCESS_KEY_ID="AKIAIZZPF5XTKUH4FN3Q" AWS_SECRET_ACCESS_KEY="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" \
#     AWS_STORAGE_BUCKET_NAME="stargate-cdn"  \
#     AWS_STORAGE_BUCKET_NAME_FOR_SWF="stargate-strongworkforce" \
#     AWS_COGNITO_USER_POOL_ID='us-east-1_fvhg6i4OV' AWS_COGNITO_CLIENT_ID='3qlj82sn3drkqlcs1r2anq6bk5' AWS_COGNITO_CLIENT_SECRET='10cfae2a92n4h4qfgldiscg1k6eorhc5t0acrftp0guebmgsgv79' \
#     AWS_COGNITO_SUPER_USER_POOL_ID="us-east-1_AAIfSp5UJ" AWS_COGNITO_SUPER_USER_CLIENT_ID='4b9ergvh17vvnf3hg9op0q5q5j' AWS_COGNITO_SUPER_USER_CLIENT_SECRET='u14vatc93hgth5ae24qv6e535ilq7uqfmsae3dsn09soaq0t4n3' \
#     CACHE_SERVER="cache"  \
#     USE_CACHE='False' \
#     SERVER_ENV='dev'\
#     CDN_SERVER='https://stargate-cdn.startmypathway.com' \
#     NON_CDN_SERVER='https://stargate-cdn.s3.amazonaws.com'\
#     SRM_BASE_URL='https://stargate-srm-dev.startmypathway.com'\
#     GPS_BASE_URL="http://gps:8000"\
#     EVENT_SURVEY_URL='https://stargate-gps-dev.startmypathway.com'\
#     LOG_DIR="/app/"\
#     ENABLE_LOGGING='False' \
#     \
#     QUIKFYND_INSTITUTE_LIST_URL='https://quikextract.azure-api.net/catalogs/v1/available_results'\
#     QUIKFYND_PDF_PARSER_SUBS_KEY='36f56b65fef64014b103a6a6923d8880'\
#     QUIKFYND_COURSE_LIST_URL='https://quikextract.azure-api.net/catalogs/v1/courses'\
#     QUIKFYND_CATALOG_SUBS_KEY='61241fe289414fd3b9ae144362d486ed'\
#     AWS_APP_SYNC_END_POINT='https://waentiexrraezbe7aybtm3ymhy.appsync-api.us-east-1.amazonaws.com/graphql'\
#     AWS_APP_SYNC_HEADER='{ "x-api-key": "da2-igncrc5razhudcqwx6cxaekijm"}'\
#     AWS_CDN_SERVER='https://stargate-cdn.s3.amazonaws.com/'


FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get -y install \
    apt-transport-https \
    ca-certificates \
    gnupg2 \
    software-properties-common
RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   $(lsb_release -cs) \
   stable"  
RUN apt-get update
RUN apt-get -y install docker-ce

USER jenkins

RUN apk add --no-cache curl make gcc libc-dev linux-headers musl-dev tk-dev tcl-dev openssl-dev libffi-dev mysql-client mariadb-dev python3-dev jpeg-dev zlib-dev freetype-dev lcms2-dev tiff-dev openjpeg-dev
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
# RUN  python /app/manage.py makemigrations SRM_User Institution && python /app/manage.py migrate && python /app/manage.py makemigrations Outreach Onboarding CareerPath && python /app/manage.py migrate && python /app/manage.py loaddata userType && python /app/manage.py loaddata outreach && python /app/manage.py loaddata institution

# CMD ["python3", "/app/manage.py", "runserver", "0.0.0.0:8000"]
CMD python3 /app/manage.py runserver 0.0.0.0:8000