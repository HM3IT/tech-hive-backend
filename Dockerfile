FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src /app
COPY db_data /var/lib/postgresql/data

EXPOSE 80

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]