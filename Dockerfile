FROM python:3-slim

MAINTAINER zocker_160

WORKDIR /home/Discordbot
VOLUME /home/Discordbot

ADD bot.py .
ADD requirements.txt .

RUN pip3 install -r requirements.txt

CMD python3 bot.py
