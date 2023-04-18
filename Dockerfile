FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install Django==3.2.2
RUN pip install -r requirements.txt
ADD . /code/
