FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /requirements /config/
RUN pip install -r /config/requirements
RUN mkdir /src;
WORKDIR /src