FROM centos:8.1.1911

EXPOSE 5000

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ARG blduser
ENV C_USER=$blduser

ENV FLASK_APP=lrnflsk:application:create_full_app()
ENV FLASK_ENV=production
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
ENV LEARN_FLASK_CONFIG=/lrnflsk/config_prod.py
ENV PYCURL_SSL_LIBRARY=openssl

RUN dnf install -y python36 python36-devel
RUN dnf install -y libcurl-devel gcc openssl-devel

# Add user for Celery to not have a super user
RUN useradd -r --uid=1001 -m ${C_USER}

COPY . /lrnflsk
WORKDIR /lrnflsk
RUN pip3.6 install -r requirements.txt
RUN python3.6 -m easy_install pycurl
RUN mkdir /var/log/lrnflsk
RUN ln -s /dev/null /var/log/lrnflsk/server.log

