FROM python:3.10-alpine

RUN adduser -D agregator

WORKDIR /home/agregator

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn

COPY app app
COPY main.py config.py boot.sh client.py ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R agregator:agregator ./
USER agregator

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]