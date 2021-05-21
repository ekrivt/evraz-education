FROM python:3

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]