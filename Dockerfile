FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py translator.py pyproject.toml ./

EXPOSE 8000

CMD ["python", "main.py"]