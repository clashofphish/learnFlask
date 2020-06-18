FROM centos:7.6.1810

EXPOSE 5000

ARG blduser
ENV C_USER=$blduser

ENV FLASK_APP=lrnflsk:create_full_app()
ENV FLASK_ENV=production
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
ENV LEARN_FLASK_CONFIG=/lrnflsk/config_prod.py

RUN yum install -y https://repo.ius.io/ius-release-el7.rpm
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip

# Add user for Celery to not have a super user
RUN useradd -r --uid=1001 ${C_USER}

COPY . /lrnflsk
WORKDIR /lrnflsk
RUN pip3.6 install -r requirements.txt
#RUN pip3.6 install -e .
#RUN pip3.6 install gunicorn
RUN mkdir /var/log/lrnflsk
RUN ln -s /dev/null /var/log/lrnflsk/server.log

#ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]