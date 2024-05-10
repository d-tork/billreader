FROM python:3.13.0a6-slim-bullseye
RUN python -m pip install -U --upgrade \
    pip \
    setuptools \
    wheel

WORKDIR /bill-pdfs
ENV PROJ_ROOT="/bill-pdfs"
ENV DATA_ROOT="/data"
ENV CONFIG_FILE="/run/config/config.yaml"
VOLUME /data

# This step not likely to change often
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY . .
RUN python -m pip install .

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION:-dev}

ENTRYPOINT ["billreader"]
