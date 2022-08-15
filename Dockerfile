# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader omw-1.4

COPY . .

ENV ENV=prod

CMD [ "sh", "start.sh"]
