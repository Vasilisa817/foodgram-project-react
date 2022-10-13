FROM python:3.7-slim
LABEL author="Vasilisa Nemoliaeva"
WORKDIR /backend

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /backend

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
