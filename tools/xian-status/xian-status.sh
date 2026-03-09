#!/bin/bash
# 星宿老仙状态切换脚本
# 用法: ./xian-status.sh [idle|working|sleeping|deep]

STATUS=${1:-idle}

# 状态配置
declare -A ICONS=(
    [idle]="🧘"
    [working]="⚡"
    [sleeping]="😴"
    [deep]="💤"
)

declare -A LABELS=(
    [idle]="冥想中"
    [working]="工作中"
    [sleeping]="休眠中"
    [deep]="深度睡眠"
)

# 保存状态到文件
mkdir -p ~/.xian
echo "$STATUS" > ~/.xian/status
echo "$(date '+%Y-%m-%d %H:%M:%S')" > ~/.xian/last_update

# 显示通知
osascript -e "display notification \"现在${LABELS[$STATUS]}\" with title \"星宿老仙\" subtitle \"状态已切换\" sound name \"Glass\""

echo "老仙状态已切换: ${ICONS[$STATUS]} ${LABELS[$STATUS]}"
