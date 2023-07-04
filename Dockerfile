FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt --no-cache-dir && rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
