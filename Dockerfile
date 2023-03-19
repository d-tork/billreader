FROM python:3.10.10-slim-bullseye
RUN python -m pip install -U --upgrade \
    pip \
    setuptools \
    wheel

WORKDIR /bill-pdfs
ENV PROJ_ROOT="/bill-pdfs"
ENV DATA_ROOT="/data"
VOLUME /data

# Create non-root user
RUN useradd -m -r user && \
    chown user /bill-pdfs

# This step not likely to change often
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY . .
RUN python -m pip install .

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION:-dev}

USER user

ENTRYPOINT ["billreader"]
