FROM python:3.6
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

CMD ['gunicorn', 'momentiio.wsgi:application']
