# Dockerfile
FROM python:3.9-alpine

# setting institute proxy 
# ENV http_proxy http://10.7.0.1:8080
# ENV https_proxy http://10.7.0.1:8080

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk add libpq-dev

WORKDIR /code

COPY requirements.txt /code/
# RUN apt-get update && apt-get upgrade -y

# RUN pip install --upgrade wheel
# RUN pip install --upgrade setuptools
# RUN pip install --upgrade setuptools
# RUN pip install -r requirements.txt --no-cache
RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:5055"]
