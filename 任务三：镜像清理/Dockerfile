FROM  python:alpine3.8
WORKDIR /data/containers/
COPY requirements.txt .
COPY DockerPrune.py .
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
ENTRYPOINT python3 DockerPrune.py