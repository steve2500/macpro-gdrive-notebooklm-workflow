#!/usr/bin/env bash

set -euo pipefail

# Set PATH for crontab compatibility
export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$PATH"

# Explicitly set rclone config location
export RCLONE_CONFIG="$HOME/.config/rclone/rclone.conf"

#######################################
# 基础路径定义
#######################################

LOCAL_BASE="/Users/yang.yang/_Syno_Attachment/SynologyDrive/__Notebookllm/PRO"
GDRIVE_BASE="gdrive_pro:Notebooklm_Pro"

LOG_DIR="$HOME/temp/log"

#######################################
# 日志保留策略（Retention）
#######################################

LOG_PREFIX="rclone_sync_"
LOG_RETENTION_DAYS=180   # ≈ 6 months

#######################################
# 动态目录数组
#######################################

DIR_ARRAY=(
  "0.Notebooklm_WIKI.20260102230129"
  # "another_dir"
)

#######################################
# 日志初始化
#######################################

mkdir -p "$LOG_DIR"
TS=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/${LOG_PREFIX}${TS}.log"

#######################################
# 日志清理模块（执行前）
#######################################

find "$LOG_DIR" \
  -type f \
  -name "${LOG_PREFIX}*.log" \
  -mtime +${LOG_RETENTION_DAYS} \
  -print \
  -delete >> "$LOG_FILE" 2>&1

#######################################
# 主同步逻辑
#######################################

for DIR_NAME in "${DIR_ARRAY[@]}"; do
  LOCAL_DIR="${LOCAL_BASE}/${DIR_NAME}"
  GDRIVE_DIR="${GDRIVE_BASE}/${DIR_NAME}"

  echo "===================================" >> "$LOG_FILE"
  echo "Start sync: $DIR_NAME" >> "$LOG_FILE"
  echo "Local  : $LOCAL_DIR" >> "$LOG_FILE"
  echo "Remote : $GDRIVE_DIR" >> "$LOG_FILE"
  echo "Time   : $(date)" >> "$LOG_FILE"

  if ! rclone sync \
    "$LOCAL_DIR" \
    "$GDRIVE_DIR" \
    --log-file="$LOG_FILE" \
    --log-level=INFO; then
    echo "ERROR: rclone sync failed for $DIR_NAME" >> "$LOG_FILE"
    echo "rclone path: $(which rclone 2>&1)" >> "$LOG_FILE"
    echo "rclone config: $RCLONE_CONFIG" >> "$LOG_FILE"
  fi
#    --stats=30s

  echo "Finish sync: $DIR_NAME" >> "$LOG_FILE"
  echo >> "$LOG_FILE"
done
