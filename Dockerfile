FROM python:3-slim

MAINTAINER zocker_160

ENV DISCORD_TOKEN <put token here>

WORKDIR /home/Discordbot
VOLUME /home/Discordbot

ADD Discord_bot.py .
ADD requirements.txt .

RUN pip3 install -r requirements.txt

CMD python3 Discord_bot.py
