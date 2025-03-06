FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
COPY ./common ./common
COPY ./producer/ ./producer
COPY ./gcp-sa.json ./gcp-sa.json
# ENV GOOGLE_APPLICATION_CREDENTIALS=gcp-sa.json
RUN pip install -r requirements.txt
CMD ["python", "-m", "producer.producer"]
