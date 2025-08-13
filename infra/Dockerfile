FROM python:3.11-slim
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
COPY pyproject.toml README.md /app/
RUN pip install --upgrade pip uv && uv pip install -e .[dev]
COPY . /app
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
