FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]