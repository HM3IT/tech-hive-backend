ARG PYTHON_BUILDER_IMAGE=3.12-bookworm

FROM python:${PYTHON_BUILDER_IMAGE} as python-base


WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "80"]