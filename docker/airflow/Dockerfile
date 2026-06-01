FROM apache/airflow:2.9.1

USER root

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_HOME=/home/airflow/.local/lib/python3.12/site-packages/pyspark
ENV PYTHONPATH=/app

USER airflow

RUN pip install --no-cache-dir \
    pyspark==3.5.1 \
    delta-spark==3.2.0 \
    pandas==2.2.2 \
    requests==2.32.3 \
    psycopg2-binary==2.9.9 \
    pyarrow==16.1.0