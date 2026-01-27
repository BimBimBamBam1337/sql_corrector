FROM python:3.13-slim

# системные пакеты (таймзона и прочее)
RUN apt-get update && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

# установка uv
RUN pip install --user uv

COPY . .

# запуск синхронизации
RUN uv sync

