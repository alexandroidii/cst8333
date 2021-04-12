FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
RUN apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /rlcs_app
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
