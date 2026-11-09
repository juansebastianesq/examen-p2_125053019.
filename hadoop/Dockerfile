# 1. Imagen base Debian actualizada
FROM debian:bookworm-slim

# 2. Instalar Java, Python 3, OpenSSH Server y herramientas
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3 \
    wget \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# 3. Instalar Hadoop standalone
RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzf hadoop-3.3.6.tar.gz && \
    mv hadoop-3.3.6 /usr/local/hadoop && \
    rm hadoop-3.3.6.tar.gz

# 4. Configurar SSH sin contraseña con llaves (Parte B)
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# Evitar confirmación estricta de host para conexiones locales
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# 5. Variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# 6. Script de inicio para arrancar SSH y mantener el contenedor vivo
CMD service ssh start && tail -f /dev/null