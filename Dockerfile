FROM python:3-onbuild
RUN pip3 install --upgrade pip

RUN git clone https://github.com/guleroman/innApi.git /API
WORKDIR /API

RUN apk add libreoffice \
	build-base \ 
	# Install fonts
	msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f

# prevent libreoffice from querying ::1 (ipv6 ::1 is rejected until istio 1.1)
RUN mkdir -p /etc/cups && echo "ServerName 127.0.0.1" > /etc/cups/client.conf

EXPOSE 6060

ENTRYPOINT ["python3", "app.py"]