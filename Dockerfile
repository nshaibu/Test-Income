FROM python:3.10.14-alpine3.20
WORKDIR /income
ENV PATH=$PATH:.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
RUN python manage.py migrate