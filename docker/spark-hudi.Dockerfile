FROM apache/spark:3.5.3-scala2.12-java17-python3-ubuntu
USER root
ARG HUDI_VERSION=1.1.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/hudi && curl -fL -o /opt/hudi/hudi-spark-bundle.jar "https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3.5-bundle_2.12/${HUDI_VERSION}/hudi-spark3.5-bundle_2.12-${HUDI_VERSION}.jar"
WORKDIR /opt/commerce
COPY . /opt/commerce
ENV PYTHONPATH=/opt/commerce/src:/opt/commerce
CMD ["bash"]
