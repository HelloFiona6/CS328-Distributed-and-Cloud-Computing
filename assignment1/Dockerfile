FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential openmpi-bin libopenmpi-dev openssh-server \
    && rm -rf /var/lib/apt/lists/*

# 非 root 用户
RUN useradd -m -s /bin/bash mpi  

# sshd 运行所需目录
RUN mkdir -p /run/sshd

# 启动脚本
COPY init-ssh.sh /usr/local/bin/init-ssh.sh
RUN chmod +x /usr/local/bin/init-ssh.sh

# 工作目录（代码将挂载进来）
WORKDIR /workspace

CMD ["/usr/local/bin/init-ssh.sh"]
