#!/bin/bash
# 老仙自我保护备份脚本
# 每次更新前执行：备份 + 提交

set -e

WORKSPACE="/Users/rocky/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE/.backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="laoxian-backup-$DATE"

echo "🐉 老仙开始自我保护备份..."

# 1. 创建本地备份目录
mkdir -p "$BACKUP_DIR"

# 2. 备份关键配置文件
echo "📦 备份配置文件..."
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
    2>/dev/null || true

# 3. Git 提交
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

# 4. 清理旧备份（保留最近10个）
echo "🧹 清理旧备份..."
ls -t "$BACKUP_DIR"/laoxian-backup-*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f

echo "✅ 老仙备份完成: $BACKUP_NAME"
echo "📍 备份位置: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
