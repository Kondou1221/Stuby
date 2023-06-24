FROM python:3.9-buster

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./api/ .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]