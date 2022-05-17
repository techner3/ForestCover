FROM python:3.7-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update 
EXPOSE 5001
ENTRYPOINT FLASK_APP=/app/app.py flask run --host 0.0.0.0