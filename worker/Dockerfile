FROM python:3.11.0-slim-buster

COPY source/ ./source/

ENV PYTHONPATH "/source"

RUN pip install -r source/requirements.txt

ENTRYPOINT ["python", "-u", "./source/worker/sandbox.py"]
