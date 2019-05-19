FROM python:3-onbuild
RUN pip3 install --upgrade pip

RUN git clone https://github.com/guleroman/innApi.git /API

EXPOSE 6060

ENTRYPOINT ["python3", "app.py"]