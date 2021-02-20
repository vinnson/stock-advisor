FROM python:3.10.0a5-alpine3.13

WORKDIR /srv

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pull.py"]
