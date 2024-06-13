[![.github/workflows/ci.yml](https://github.com/made-mlops-2022/artem_ustsov/actions/workflows/ci.yml/badge.svg)](https://github.com/made-mlops-2022/artem_ustsov/actions/workflows/ci.yml)

# VK Technopark-BMSTU | SEM II, ML OPS | HW_2

================================================================.  
Усцов Артем Алексеевич.  
Группа ML-21.

Преподаватели: Михаил Марюфич


### Quick Start:
Build a docker image from `online_inference/`
~~~
cd online_inference
docker build -t totenkaff/online_inference:v2 .
~~~

(Or) Pull a docker image from docker-hub
~~~
cd online_inference
docker pull totenkaff/online_inference:v2
~~~

### Quick Run:
~~~
cd online_inference
docker run --name online_inference -p 8000:8000 totenkaff/online_inference:v2
~~~
Service-swagger is available now on http://127.0.0.1:8000/docs


### Quick Tests:
- request
~~~
python3 requests/make_requests.py
~~~

- model prediction
~~~
docker exec -it online_inference bash
python3 -m pytest tests/main_request_test.py
~~~

### Docker Optimisation
1. Base image  
Build time: 169.5s  
Size: ~4000 MB


2. Use only necessary dependencies: [[v1]](https://hub.docker.com/layers/totenkaff/online_inference/v1/images/sha256-ba98a4ad860fd2a45403bc1beded305a9ae98f44a049d41672730a66634928f5?context=repo)  
Build time: 34.2s (-396% from base)  
Size: 1659 MB (-141% from base)


3. Use only lightless versions of your distributive: [[v2]](https://hub.docker.com/layers/totenkaff/online_inference/v2/images/sha256-a8edc45113c466b92ea9f88f71b2918224454b6343df2450aa820971cda398cd?context=repo)  
Build time: 30.2 s (-13% from v1)  
Size: 689 MB (-140% from v1)
>>>>>>> d23d7ab (api, schema, docker, requests are ready)
