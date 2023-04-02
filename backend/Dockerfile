FROM python:3.11.2
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]