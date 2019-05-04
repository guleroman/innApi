FROM python:3-onbuild
RUN pip3 install --upgrade pip

RUN git clone https://github.com/guleroman/innApi.git /API
WORKDIR /API

EXPOSE 5000

ENTRYPOINT ["python3", "app_2.py"]