FROM python:3.8.1

WORKDIR leggo-content

COPY ./requirements.txt requirements.txt

RUN apt-get update -y && \
    apt install python3-pip -y && \
    python -m pip --no-cache install -r requirements.txt

RUN apt-get install bash-completion
RUN apt-get install libgl1-mesa-glx libnss3 libxcomposite-dev -y
RUN wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh

COPY . .