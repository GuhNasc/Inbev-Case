FROM apache/airflow:2.1.0

USER root

# Instalar dependências
RUN apt-get update \
    && apt-get install -y sudo python3-pandas net-tools openjdk-11-jdk-headless procps curl telnet ca-certificates-java netcat \
    && apt-get install -y --fix-missing \
    && apt-get clean

# Corrigir problemas de certificados Java
RUN apt-get install -y openjdk-11-jdk \
    && apt-get clean

# Instalar Spark
RUN curl -O https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz \
    && tar -xvf spark-3.1.2-bin-hadoop3.2.tgz -C /opt/ \
    && mv /opt/spark-3.1.2-bin-hadoop3.2 /opt/spark \
    && rm spark-3.1.2-bin-hadoop3.2.tgz

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$PATH"

# Adicionar usuário airflow ao grupo sudo
RUN usermod -aG sudo airflow

# Configurar sudoers para permitir que o usuário airflow use sudo sem senha
RUN echo 'airflow ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER airflow
