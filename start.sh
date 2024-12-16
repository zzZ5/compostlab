#!/bin/bash

# 设置日志文件
LOGFILE="/var/log/compostlab_startup.log"

# 获取当前时间
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# 记录日志函数
log() {
    echo "$timestamp - $1"
}

log "Starting the CompostLab website..."

# 1. 启动 Nginx 服务
log "Starting Nginx..."
sudo systemctl start nginx
if [ $? -eq 0 ]; then
    log "Nginx started successfully."
else
    log "Failed to start Nginx."
    exit 1
fi

# 2. 启动 uWSGI 服务（使用虚拟环境中的 uWSGI）
log "Starting uWSGI..."
/srv/compostlab/.venv/bin/uwsgi --ini /srv/compostlab/uwsgi.ini &
if [ $? -eq 0 ]; then
    log "uWSGI started successfully."
else
    log "Failed to start uWSGI."
    exit 1
fi

# 3. 启动 Django 脚本 (mqtt)
log "Starting Django MQTT script..."
/srv/compostlab/.venv/bin/python /srv/compostlab/manage.py runscript mqtt &
if [ $? -eq 0 ]; then
    log "Django MQTT script started successfully."
else
    log "Failed to start Django MQTT script."
    exit 1
fi

log "All services started successfully."