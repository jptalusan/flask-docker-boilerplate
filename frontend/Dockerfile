FROM balenalib/raspberrypi3-python:3.6.6-stretch-build

EXPOSE 5011

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

RUN pip install gunicorn
