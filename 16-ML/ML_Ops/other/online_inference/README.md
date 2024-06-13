# Homework №2
### _To build image_
From source: from `online_inference/` run:
```
docker build -t lizaavsyannik/online_inference:v5 .
```

From DockerHub:
```
docker pull lizaavsyannik/online_inference:v5
```

### _To run container_
```
docker run --name inference -p 8000:8000 lizaavsyannik/online_inference:v5
```
Now service is running on _http://127.0.0.1:8000/docs_

### _To make requests_
Open new terminal, from `online_inference/` run:
```
python3 requests/make_requests.py
```
### _To run tests_
```
docker exec -it inference bash
python3 -m pytest test_main.py
```
### _Docker Image Size Optimizations_
1. Practice: Don’t install unnecessary packages  
    Implementation: _requirements.txt_ contains only necessary packages  
    Result [v1](https://hub.docker.com/layers/lizaavsyannik/online_inference/v1/images/sha256-7256dead3136bf6e13b8f0e5a89467aae2e702fd2f0ffd7944a7023fd78f081e?context=repo): Compressed Size 566.67 MB 
2. Practice: Minimize the number of layers  
    Implementation: used only one COPY instruction for all files that need to be copied  
    Result [v2](https://hub.docker.com/layers/lizaavsyannik/online_inference/v2/images/sha256-15b94d131b1a8ef9cfe12aa15896bf84798af697d7a7302dd383d441c9c7c710?context=repo): Compressed Size 566.67 MB (didn't really make a difference in this case)
3. Practice: Exclude files from context using .dockerignore  
    Implementation: excluded all files that don't need to be copied  
    Result [v3](https://hub.docker.com/layers/lizaavsyannik/online_inference/v3/images/sha256-15b94d131b1a8ef9cfe12aa15896bf84798af697d7a7302dd383d441c9c7c710?context=repo): Compressed Size 566.67 MB (didn't really make a difference in this case)
4. Practice: Choose more lightweight basis  
    Implementation: used python:3.8.15-slim-buster  
    Result [v4](https://hub.docker.com/layers/lizaavsyannik/online_inference/v4/images/sha256-15b94d131b1a8ef9cfe12aa15896bf84798af697d7a7302dd383d441c9c7c710?context=repo): Compressed Size 276.05 MB (significant improvement)
