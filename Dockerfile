FROM python:3.8.1

WORKDIR leggo_content

COPY ./requirements.txt requirements.txt

RUN apt-get update -y && \
    apt install python3-pip -y && \
    python -m pip --no-cache install -r requirements.txt

COPY . .