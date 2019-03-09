ARG ACCESSIFY_PYTHON_VERSION

FROM python:$ACCESSIFY_PYTHON_VERSION

WORKDIR /accessify
COPY . /accessify

RUN pip3 install -r requirements-dev.txt
RUN pip3 install -r requirements-tests.txt

CMD sleep 7200
