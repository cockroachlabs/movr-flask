FROM python:3.8

COPY movr ./movr
COPY static ./static
COPY templates ./templates
COPY web ./web
COPY __init__.py ./
COPY movr.yaml ./
COPY requirements.txt ./
COPY server.py ./

RUN pip install -r requirements.txt

ENV DEBUG 'False'
ENV SECRET_KEY 'key'

EXPOSE 8080

CMD ["gunicorn", "-c", "/web/gunicorn.py", "server:app"]
