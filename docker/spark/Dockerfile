FROM apache/spark:3.5.1

USER root

COPY docker/spark/requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

ENV HOME=/tmp
ENV IVY_HOME=/tmp/.ivy2

RUN mkdir -p /tmp/.ivy2 && chmod -R 777 /tmp/.ivy2

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]