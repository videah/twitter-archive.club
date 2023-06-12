FROM python:3.11.4

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

COPY . /app
WORKDIR /app

RUN poetry install --no-interaction --no-ansi

ENTRYPOINT ["./gunicorn.sh"]