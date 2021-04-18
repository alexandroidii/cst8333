FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

COPY requirements.txt .
# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
RUN pip3 install -r /requirements.txt
RUN apk del .build-deps

WORKDIR /rlcs_app
COPY . .

COPY ./scripts /scripts

RUN chmod +x /scripts/*
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]