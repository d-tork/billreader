FROM python:3.7.8-slim-buster
RUN python -m pip install -U --upgrade \
    pip \
    setuptools \
    wheel

WORKDIR /bill-pdfs

# Create non-root user
RUN useradd -m -r user && \
    chown user /bill-pdfs

# This step not likely to change often
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

COPY . .
RUN python -m pip install .

RUN mkdir /common
USER user

ENTRYPOINT ["billreader"]