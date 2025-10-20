#!/usr/bin/env bash
set -e

# 1) 启动 sshd（先启动，不影响后续）
/usr/sbin/sshd

# 2) 用 root 确保目录存在且归 mpi 所有（卷首次创建默认是 root:root）
mkdir -p /home/mpi/.ssh
chown -R mpi:mpi /home/mpi/.ssh
chmod 700 /home/mpi/.ssh

# 3) 切到 mpi 用户生成密钥 & 配置
su - mpi -c '
  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
  fi
  grep -q "$(cat ~/.ssh/id_rsa.pub)" ~/.ssh/authorized_keys 2>/dev/null || \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

  echo -e "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null" > ~/.ssh/config

  chmod 600 ~/.ssh/authorized_keys ~/.ssh/config
'

# 4) 保持前台
tail -f /dev/null
