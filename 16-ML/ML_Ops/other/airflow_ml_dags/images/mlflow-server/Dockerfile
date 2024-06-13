FROM python:3.8.15-slim-buster

WORKDIR /mlflow/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV BACKEND_URI sqlite:///:memory
ENV ARTIFACT_ROOT ./mlruns

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0 --port 5000
