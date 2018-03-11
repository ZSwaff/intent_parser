FROM ubuntu:16.04
RUN apt-get update \
  && apt-get install -y python3-pip python-dev build-essential
RUN pip3 install flask
VOLUME /home/ubuntu/flask
CMD "python3 /home/ubuntu/flask/app.py"
