FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/

COPY src/requirements.txt ./requirements.txt
RUN python3 -m pip install --root-user-action=ignore --no-cache-dir --upgrade pip && \
    python3 -m pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

COPY src/ ./

CMD [ "python3", "main.py" ]