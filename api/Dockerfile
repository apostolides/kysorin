FROM python:3.7

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

WORKDIR /api

COPY . /api/

RUN pip install -r requirements.txt
RUN pip install "fastapi[all]"

WORKDIR /geckodriver
COPY ./geckodriver /geckodriver/

EXPOSE 8000

WORKDIR /api
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]