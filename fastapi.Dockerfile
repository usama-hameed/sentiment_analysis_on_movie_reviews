FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python -m spacy download en_core_web_sm

CMD ["uvicorn", "routers:app", "--host", "0.0.0.0", "--port", "8000"]
