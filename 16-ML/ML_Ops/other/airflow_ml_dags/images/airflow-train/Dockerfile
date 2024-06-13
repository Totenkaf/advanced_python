FROM python:3.8.15-slim-buster
RUN python3 -m pip install --upgrade pip

COPY train.py requirements.txt /

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "train.py"]
