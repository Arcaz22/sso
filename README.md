#!/usr/bin/env bash
set -e

OWNER=$1
PROJECT=$2

BASE_DIR="/home/deploy/apps"
LOG_DIR="/home/deploy/logs"

cd "$BASE_DIR/$OWNER/$PROJECT"

echo "[$(date)] Deploy $OWNER/$PROJECT" >> "$LOG_DIR/deploy.log"

git pull origin main
docker compose build
docker compose up -d

echo "[$(date)] Deploy selesai" >> "$LOG_DIR/deploy.log"
