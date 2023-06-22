FROM python:3.11.1

WORKDIR /user/src/app

COPY  req   ./ 
# ./ == WORKDIR 

RUN pip install --no-cache-dir -r req
 
COPY .  .
# 변경된 단계부터 작업이 시작되므로 주의하여 순서배정.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t fast-1 . 

