FROM docker.io/library/python:3.10

WORKDIR /app/

COPY ./app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#COPY ./app /code/app
COPY ./app /app
ENV PYTHONPATH=/app

#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
