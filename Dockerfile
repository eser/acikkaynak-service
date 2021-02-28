###########
# BUILDER #
###########

FROM python:3-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev libffi-dev --no-install-recommends

RUN pip install pipenv

COPY . .

RUN pipenv lock --requirements > requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt



#########
# FINAL #
#########

FROM python:3-slim

ENV PORT=8000
ENV APP_HOME=/home/app

RUN apt-get update && apt-get install -qq -y \
  gdal-bin --no-install-recommends

RUN mkdir -p $APP_HOME
RUN groupadd -r app
RUN useradd -r -g app app

WORKDIR $APP_HOME

COPY --from=builder /usr/src/app .
RUN chown -R app:app $APP_HOME

RUN pip install --no-cache ./wheels/*
RUN pip install gunicorn

USER app
EXPOSE 8000

ENTRYPOINT ["/home/app/entrypoint.sh"]
