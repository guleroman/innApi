FROM python:3-onbuild
#RUN pip3 install --upgrade pip
RUN pip3 install requests bs4

RUN git clone https://github.com/guleroman/innApi.git /API

WORKDIR /API

#ARG inn

EXPOSE 8888




ENTRYPOINT ["python3", "innApi.py"]