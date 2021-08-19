FROM python:3.8

COPY movr ./movr
COPY static ./static
COPY templates ./templates
COPY web ./web
COPY __init__.py ./
COPY requirements.txt ./
COPY server.py ./
COPY certs ./certs

RUN pip install -r requirements.txt

ENV DEBUG 'False'
ENV SECRET_KEY 'key'

CMD ["gunicorn", "-c", "/web/gunicorn.py", "server:app"]
