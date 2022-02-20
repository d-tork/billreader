FROM python:3.7.11-slim-buster
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

USER user

ENTRYPOINT ["billreader"]