FROM python:3.10-slim-bullseye
RUN python3 -m pip install --upgrade pip

COPY main.py schema.py tests requests run.sh requirements.txt ./online_inference/

WORKDIR /online_inference

RUN apt-get update && apt-get install wget -y
RUN pip3 install -r requirements.txt

ENV PATH_TO_MODEL="LogisticRegressionCV_model.pkl"
#  s3_bucket: ml_project
#  s3_endpoint_url: "https://hb.bizmrg.com"
#  aws_access_key_id: "6CKG3ZF3Mxs91VfNrw3c9Z"
#  aws_secret_access_key: "47vCFUUq3su1EhCeLzpXDDL2iBvtV6DudxJDcNsh9kKp"
# dckr_pat_k_SSlnwQYZLeZMW9swamtrz9vbQ - docker token

EXPOSE 8000

CMD ["bash", "run.sh"]
