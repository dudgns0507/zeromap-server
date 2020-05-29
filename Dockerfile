FROM ubuntu:18.04
MAINTAINER your_name "hoon2585@gmail.com"

ENV LANG C.UTF-8

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev python3-venv libmysqlclient-dev

RUN python3.6 -m pip install pip --upgrade

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
