FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
COPY ./common ./common
COPY ./api ./api
COPY ./gcp-sa.json ./gcp-sa.json
# ENV GOOGLE_APPLICATION_CREDENTIALS=gcp-sa.json
RUN pip install --no-cache-dir -r ./requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


