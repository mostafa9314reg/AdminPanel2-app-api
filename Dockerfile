# FROM python:3.11.7-alpine3.19
FROM python:3.10.13-alpine3.19

LABEL maintainer="adminpanle2"

ENV PYTHONUNBUFFERED 1

COPY ./requierments.txt  /tmp/requierments.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app  /app

WORKDIR  /app

EXPOSE 9000

ARG DEV=false

RUN  python -m venv /py  && \
 /py/bin/pip install --upgrade pip && \
 apk add --update --no-cache postgresql-client  && \
 apk add --update --no-cache --virtual .tmp-build-deps \
       build-base postgresql-dev musl-dev  && \
 /py/bin/pip install -r /tmp/requierments.txt && \
 if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
 fi && \
 rm -rf /tmp && \
 apk del .tmp-build-deps && \
 adduser  \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user


