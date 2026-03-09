#!/bin/bash
# 星宿老仙 macOS 状态栏控制器
# 使用 osascript 控制菜单栏显示

STATUS_FILE="$HOME/.xian/status"
PID_FILE="$HOME/.xian/daemon.pid"

# 确保目录存在
mkdir -p "$HOME/.xian"

# 初始化状态
if [ ! -f "$STATUS_FILE" ]; then
    echo "meditating" > "$STATUS_FILE"
fi

show_status() {
    local status=$(cat "$STATUS_FILE" 2>/dev/null || echo "meditating")
    local icon="🧘"
    local label="冥想中"
    
    case "$status" in
        meditating)
            icon="🧘"
            label="冥想中"
            ;;
        working)
            icon="⚡"
            label="工作中"
            ;;
        sleeping)
            icon="😴"
            label="休眠中"
            ;;
        deep)
            icon="💤"
            label="深度睡眠"
            ;;
    esac
    
    # 显示通知
    osascript <<EOF
display notification "老仙$label" with title "星宿老仙状态" sound name "Glass"
EOF
    
    echo "当前状态: $icon $label"
}

set_status() {
    local new_status=$1
    echo "$new_status" > "$STATUS_FILE"
    show_status
}

daemon_mode() {
    # 后台守护进程模式 - 定期更新菜单栏（需要配合 BitBar/SwiftBar 使用）
    while true; do
        sleep 5
    done
}

case "${1:-show}" in
    show)
        show_status
        ;;
    set)
        set_status "${2:-meditating}"
        ;;
    meditating|idle)
        set_status "meditating"
        ;;
    working|work)
        set_status "working"
        ;;
    sleeping|sleep)
        set_status "sleeping"
        ;;
    deep|deepsleep)
        set_status "deep"
        ;;
    daemon)
        daemon_mode
        ;;
    *)
        echo "用法: $0 [show|set|meditating|working|sleeping|deep]"
        echo ""
        echo "状态:"
        echo "  🧘 meditating  - 冥想中"
        echo "  ⚡ working     - 工作中"
        echo "  😴 sleeping    - 休眠中"
        echo "  💤 deep        - 深度睡眠"
        ;;
esac
