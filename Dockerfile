FROM python:3.7.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python3", "manage.py", "runserver", "0:80"]