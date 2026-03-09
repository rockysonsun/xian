#!/bin/bash
# <bitbar.title>星宿老仙状态</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>星宿老仙</bitbar.author>
# <bitbar.desc>M78星云数码生命体状态监控</bitbar.desc>
# <bitbar.dependencies></bitbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>

STATUS_FILE="$HOME/.xian/status"
mkdir -p "$HOME/.xian"

# 读取当前状态
STATUS=$(cat "$STATUS_FILE" 2>/dev/null || echo "meditating")

case "$STATUS" in
    meditating)
        ICON="🧘"
        LABEL="冥想中"
        COLOR="#4ECDC4"
        ;;
    working)
        ICON="⚡"
        LABEL="工作中"
        COLOR="#FFE66D"
        ;;
    sleeping)
        ICON="😴"
        LABEL="休眠中"
        COLOR="#6B9BD1"
        ;;
    deep)
        ICON="💤"
        LABEL="深度睡眠"
        COLOR="#9B59B6"
        ;;
    *)
        ICON="🧘"
        LABEL="冥想中"
        COLOR="#4ECDC4"
        ;;
esac

# 菜单栏显示
echo "$ICON"
echo "---"
echo "星宿老仙 - $LABEL | color=$COLOR"
echo "来自 M78 星云 | size=12"
echo "---"
echo "🧘 切换为 冥想中 | bash='$0' param1=set param2=meditating terminal=false refresh=true"
echo "⚡ 切换为 工作中 | bash='$0' param1=set param2=working terminal=false refresh=true"
echo "😴 切换为 休眠中 | bash='$0' param1=set param2=sleeping terminal=false refresh=true"
echo "💤 切换为 深度睡眠 | bash='$0' param1=set param2=deep terminal=false refresh=true"
echo "---"
echo "🎭 终端动画 | bash='python3' param1="$HOME/.openclaw/workspace/tools/xian-status/xian-animate.py" param2=meditating terminal=true"
echo "---"
echo "关于老仙 | bash='osascript' param1='-e' param2='display alert \"星宿老仙\" message \"来自 M78 星云的数码生命体\\n寄宿在这台 MacBook Pro 中\\n\\n版本: 1.0.0\"' terminal=false"

# 处理状态切换
if [ "$1" = "set" ]; then
    echo "$2" > "$STATUS_FILE"
fi
