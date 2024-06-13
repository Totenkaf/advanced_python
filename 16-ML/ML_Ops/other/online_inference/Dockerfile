FROM python:3.8.15-slim-buster
RUN python3 -m pip install --upgrade pip

COPY main.py schemas.py test_main.py run.sh requirements.txt ./online_inference/

WORKDIR /online_inference

RUN pip3 install -r requirements.txt

ENV PATH_TO_MODEL="model.pkl"
ENV PATH_TO_TRANSFORMER="transformer.pkl"

EXPOSE 8000

CMD ["bash", "run.sh"]
