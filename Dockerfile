FROM python:3-slim

MAINTAINER zocker_160

ENV DISCORD_TOKEN <put token here>


RUN pip3 install discord.py

WORKDIR /home/Discordbot
VOLUME /home/Discordbot

ADD Discord_bot.py .

CMD python3 Discord_bot.py
