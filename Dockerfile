FROM python:3-alpine

ENV APP_HOME /API
WORKDIR $APP_HOME

RUN apk add libreoffice \
	build-base \ 
	git \
	# Install fonts
	msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f

RUN pip install Flask requests
RUN git clone https://github.com/guleroman/innApi.git /API
COPY . $APP_HOME

# prevent libreoffice from querying ::1 (ipv6 ::1 is rejected until istio 1.1)
#RUN mkdir -p /etc/cups && echo "ServerName 127.0.0.1" > /etc/cups/client.conf

EXPOSE 6060

ENTRYPOINT ["python", "app.py"]