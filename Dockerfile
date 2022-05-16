FROM python:3.7-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT FLASK_APP=/app/app.py flask run --host 0.0.0.0
EXPOSE 3000