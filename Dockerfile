FROM centos:7.8.2003

EXPOSE 5000

ARG blduser
ENV C_USER=$blduser

ENV FLASK_APP=lrnflsk:create_full_app()
ENV FLASK_ENV=production
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
ENV LEARN_FLASK_CONFIG=/lrnflsk/config_prod.py
ENV PYCURL_SSL_LIBRARY=openssl

RUN yum install -y https://repo.ius.io/ius-release-el7.rpm
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip
RUN yum install -y curl-devel gcc openssl-devel
# libcurl-devel

# Add user for Celery to not have a super user
RUN useradd -r --uid=1001 -m ${C_USER}

COPY . /lrnflsk
WORKDIR /lrnflsk
RUN pip3.6 install -r requirements.txt
RUN pip3.6 install 'pycurl==7.43.0.5' --no-cache-dir
#RUN pip3.6 install -e .
#RUN pip3.6 install gunicorn
RUN mkdir /var/log/lrnflsk
RUN ln -s /dev/null /var/log/lrnflsk/server.log

