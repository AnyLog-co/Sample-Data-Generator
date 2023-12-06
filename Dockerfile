FROM python:3.8-alpine

WORKDIR /app
RUN mkdir -p /app/Sample-Data-Generator/src

COPY requirements.txt /app/Sample-Data-Generator/requirements.txt
COPY pyproject.toml /app/Sample-Data-Generator/pyproject.toml
COPY setup.cfg /app/Sample-Data-Generator/setup.cfg
COPY setup.py  /app/Sample-Data-Generator/setup.py
COPY src/ /app/Sample-Data-Generator/src

# Install required packages
RUN apk update && \
    apk add build-base libffi-dev  py3-pip python3-dev musl-dev jpeg-dev zlib-dev libressl-dev libwebp-dev libxslt-dev \
     libxml2-dev libpq libstdc++ bash && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /app/Sample-Data-Generator/requirements.txt && \
    python3 -m pip install --upgrade setuptools Cython poetry

ENTRYPOINT ["bash"]
#ENTRYPOINT bash /app/run.sh