FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .
COPY run.sh .

# Install required packages
RUN apk update && \
    apk add build-base libffi-dev  py3-pip python3-dev musl-dev jpeg-dev zlib-dev libressl-dev libwebp-dev libxslt-dev \
     libxml2-dev libpq libstdc++ bash && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r requirements.txt

ENTRYPOINT bash /app/run.sh