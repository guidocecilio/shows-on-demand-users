# FROM python:3.6.1

# # install environment dependencies
# RUN apt-get update -yqq \
FROM python:3.6.1

# install environment dependencies
RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
    netcat \
  && apt-get -q clean

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add entrypoint.sh
ADD ./entrypoint.sh /usr/src/app/entrypoint.sh

# add app
ADD . /usr/src/app

RUN python3.6 setup.py develop --user

# run server
CMD ["sh", "./entrypoint.sh"]