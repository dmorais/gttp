FROM python:3.8

LABEL maintainer="david.morais@calculquebec.ca"

COPY ./requirements.txt /home/gttp/requirements.txt

ADD app /home/gttp/

WORKDIR /home/gttp/

RUN pip install -r requirements.txt

COPY . /home/gttp/

CMD ["python", "./app/gttp.py", "-y", "./test/test.galaxy.yml", "-s", "10"]