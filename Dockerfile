FROM python:3.8

COPY . /

RUN pip install -r requirements.txt

ENV DEBUG 'False'
ENV SECRET_KEY 'key'

EXPOSE 8080
