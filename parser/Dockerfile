FROM python:3.12-slim

RUN apt-get update
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "scheduler.py"]