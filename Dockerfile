FROM ubuntu:latest
MAINTAINER Ted Johansson "tedjohanssondeveloper@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.py
ENTRYPOINT ["python3"]
CMD ["run_api.py"]