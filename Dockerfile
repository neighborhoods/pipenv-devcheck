FROM python:3
WORKDIR /usr/src/app

COPY . .
RUN pip install pipenv
RUN pipenv install --dev --ignore-pipfile --system
