FROM python

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r req.txt

EXPOSE 80

CMD ["python", "/app/crm/manage.py", "runserver", "0.0.0.0:80"]
CMD ["python", "/app/bot/app.py"]