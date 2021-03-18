FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /todolist

COPY Pipfile* /todolist/
WORKDIR /todolist/

RUN pip install pipenv && pipenv install --system --ignore-pipfile --dev

COPY . /todolist/

RUN apt-get update && apt-get install netcat-openbsd -y

RUN chmod +x /todolist/entrypoint.sh
ENTRYPOINT ["/todolist/entrypoint.sh"]

EXPOSE 8000
