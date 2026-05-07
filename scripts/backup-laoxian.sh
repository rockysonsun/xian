#!/bin/bash
# 老仙自我保护备份脚本
# 每次更新前执行：备份 + 提交
# 支持每日自动备份（已备份则跳过）

set -e

WORKSPACE="/Users/rocky/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE/.backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="laoxian-backup-$DATE"
TODAY=$(date +%Y%m%d)

echo "🐉 老仙开始自我保护备份..."

# 检查今日是否已备份
if ls "$BACKUP_DIR"/laoxian-backup-${TODAY}_*.tar.gz 1>/dev/null 2>&1; then
    echo "✅ 今日 ($TODAY) 已备份，跳过"
    exit 0
fi

# 1. 创建本地备份目录
mkdir -p "$BACKUP_DIR"

# 2. 备份关键配置文件
echo "📦 备份工作区配置..."
tar czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
    -C "$WORKSPACE" \
    IDENTITY.md \
    USER.md \
    MEMORY.md \
    SOUL.md \
    AGENTS.md \
    TOOLS.md \
    HEARTBEAT.md \
    memory/ \
    skills/ \
    scripts/ \
    api/ \
    data/ \
    database/ \
    reports/ \
    designs/ \
    frontend/ \
    notes/ \
    state/ \
    tools/ \
    .gitignore \
    2>/dev/null || true

# 3. 备份 OpenClaw 核心配置（灾难恢复关键）
echo "🔐 备份 OpenClaw 核心配置..."
OPENCLAW_HOME="${HOME}/.openclaw"
if [ -d "$OPENCLAW_HOME" ]; then
    tar czf "$BACKUP_DIR/$BACKUP_NAME-openclaw.tar.gz" \
        -C "$OPENCLAW_HOME" \
        openclaw.json \
        openclaw.json.bak \
        openclaw.json.last-good \
        .env \
        cron/ \
        plugins/ \
        agents/ \
        identity/ \
        canvas/ \
        devices/ \
        acpx/ \
        memory/ \
        2>/dev/null || true
    echo "✅ OpenClaw 配置已备份（含向量记忆）"
else
    echo "⚠️ 未找到 OpenClaw 主目录"
fi

# 4. Git 提交
cd "$WORKSPACE"

echo "📝 检查变更..."
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ 没有变更需要提交"
else
    echo "💾 提交到 Git..."
    git add -A
    git commit -m "老仙备份: $DATE - 自动保存状态" || echo "提交完成"
    
    # 如果有远程仓库，尝试推送
    if git remote get-url origin 2>/dev/null; then
        echo "🚀 推送到远程..."
        git push origin $(git branch --show-current) 2>/dev/null || echo "⚠️ 推送失败，已本地保存"
    fi
fi

# 5. 清理旧备份（保留最近10个）
echo "🧹 清理旧备份..."
ls -t "$BACKUP_DIR"/laoxian-backup-*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f
ls -t "$BACKUP_DIR"/laoxian-backup-*-openclaw.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f
ls -t "$BACKUP_DIR"/laoxian-backup-test-*.tar.gz 2>/dev/null | xargs -r rm -f

echo "✅ 老仙备份完成!"
echo "📍 工作区备份: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
echo "📍 核心配置备份: $BACKUP_DIR/$BACKUP_NAME-openclaw.tar.gz"
