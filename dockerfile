FROM python:latest

RUN mkdir -p /usr/
WORKDIR /usr/src/
COPY src/requirements.txt ./requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY src/ ./

CMD [ "python3", "main.py" ]