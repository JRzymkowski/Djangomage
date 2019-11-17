FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install django psycopg2
COPY . /app/
EXPOSE 8100
RUN 'sleep' '3s'
CMD /app/run.sh
