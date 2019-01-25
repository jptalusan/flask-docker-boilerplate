FROM linusmotu/arm-pi-datascience:1.0.0

EXPOSE 5013

RUN mkdir -p /usr/scr/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip3 install -r requirements.txt