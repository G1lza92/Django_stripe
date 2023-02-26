FROM python:3.7-slim
WORKDIR /django_app
COPY requirements.txt ./
RUN pip install -r ./requirements.txt --no-cache-dir
COPY ./ ./
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]