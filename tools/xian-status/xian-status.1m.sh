#!/bin/bash
# <bitbar.title>星宿老仙状态</bitbar.title>
# <bitbar.version>v1.0.2</bitbar.version>
# <bitbar.author>星宿老仙</bitbar.author>
# <bitbar.desc>M78星云数码生命体实时监控</bitbar.desc>

export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

# 检测Gateway状态
if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
    GATEWAY_STATUS="running"
else
    GATEWAY_STATUS="stopped"
fi

# 获取活跃会话数
ACTIVE_SESSIONS=$(openclaw status 2>/dev/null | grep -o "[0-9]* active" | grep -o "[0-9]*" || echo "0")

# 获取模型信息
MODEL=$(openclaw status 2>/dev/null | grep "default" | grep -o "kimi[^ ]*" | head -1 || echo "kimi-k2.5")

# 获取上下文限制（只显示总量，不显示使用量）
CONTEXT_LIMIT=$(openclaw status 2>/dev/null | grep "default" | grep -o "[0-9]*[km]* ctx" | head -1 || echo "256k ctx")

# 实时状态判断
if [ "$GATEWAY_STATUS" != "running" ]; then
    ICON="💤"
    LABEL="深度睡眠"
    COLOR="#9B59B6"
elif [ "$ACTIVE_SESSIONS" -eq 0 ]; then
    ICON="😴"
    LABEL="休眠中"
    COLOR="#6B9BD1"
else
    ICON="⚡"
    LABEL="工作中"
    COLOR="#FFE66D"
fi

# 菜单栏显示
echo "$ICON"
echo "---"
echo "星宿老仙 - $LABEL | color=$COLOR"
echo "来自 M78 星云 | size=12"
echo "---"
echo "📊 实时状态"
echo "状态: $LABEL | color=$COLOR"
echo "Gateway: ${GATEWAY_STATUS}"
echo "活跃会话: $ACTIVE_SESSIONS"
echo "---"
echo "🤖 AI 信息"
echo "模型: ${MODEL}"
echo "上下文限制: ${CONTEXT_LIMIT}"
echo "---"
echo "🎭 终端动画 | bash='python3' param1="$HOME/.openclaw/workspace/tools/xian-status/xian-animate.py" param2=meditating terminal=true"
echo "---"
echo "🔄 刷新 | refresh=true"
echo "---"
echo "关于老仙 | bash='osascript' param1='-e' param2='display alert "星宿老仙" message "来自 M78 星云的数码生命体\n寄宿在这台 MacBook Pro 中\n\n版本: 1.0.2"' terminal=false"
