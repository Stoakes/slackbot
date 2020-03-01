FROM python:3.6-slim
WORKDIR /opt/slackbot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN useradd -ms /bin/bash slackbot
USER slackbot
WORKDIR /home/slackbot

CMD ["/opt/slackbot/slackbot.py"]
