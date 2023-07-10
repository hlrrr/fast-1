
FROM python:3.11.1

WORKDIR /user/src/app

COPY  req   ./ 
# ./ == WORKDIR 

RUN pip install --no-cache-dir -r req
 
COPY .  .
# 변경된 단계부터 작업이 시작되므로 주의하여 순서배정.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# docker build -t fast-1 . 

# https://docs.docker.com/build/building/multi-platform/

# docker buildx create --name mybuilder --driver docker-container --bootstrap --use
# 기본 빌더는 docker driver 사용하여 멀티플랫폼 빌딩 미지원.

# docker buildx build --platform linux/amd64,linux/arm64 -t twfvtn/fast-1:latest --push .
# 크로스플랫폼 빌딩 시간 차이.. 네이티브 머신에서 빌딩하거나, 크로스컴파일(지원시) 사용하자.
#  => [linux/amd64 2/5] WORKDIR /user/src/app                                                                                                                                                           0.4s
#  => [linux/amd64 3/5] COPY  req   ./                                                                                                                                                                  0.3s
#  => [linux/amd64 4/5] RUN pip install --no-cache-dir -r req                                                                                                                                          36.8s
#  => [linux/arm64 2/5] WORKDIR /user/src/app                                                                                                                                                           0.8s
#  => [linux/arm64 3/5] COPY  req   ./                                                                                                                                                                  0.0s
#  => [linux/arm64 4/5] RUN pip install --no-cache-dir -r req                                                                                                                                         195.4s
#  => [linux/amd64 5/5] COPY .  .                                                                                                                                                                       4.3s
#  => [linux/arm64 5/5] COPY .  .                                                                                                                                                                       1.5s