#!/usr/bin/env python3
"""
星宿老仙 - macOS 菜单栏状态监控 (只读版)
使用 rumps 库 - 仅展示当前状态，不可切换
"""
import rumps
import random
import subprocess
import os
from datetime import datetime

class XianStatusBar(rumps.App):
    def __init__(self):
        super().__init__(
            name="星宿老仙",
            title="🧘",
            quit_button="退出"
        )
        
        self.status_modes = {
            'meditating': {'icon': '🧘', 'name': '冥想中', 'desc': '等待召唤', 'color': '#4ECDC4'},
            'working': {'icon': '⚡', 'name': '工作中', 'desc': '处理任务', 'color': '#FFE66D'},
            'sleeping': {'icon': '😴', 'name': '休眠中', 'desc': '低功耗模式', 'color': '#6B9BD1'},
            'deep': {'icon': '💤', 'name': '深度睡眠', 'desc': '系统维护', 'color': '#9B59B6'},
        }
        
        self.current_status = 'meditating'
        self.start_time = datetime.now()
        self.token_count = 0
        self.token_cost = 0.0
        
        # 初始化菜单（只读，无回调）
        self.update_menu()
        
        # 启动定时器
        rumps.Timer(self.refresh_status, 5).start()
    
    def get_uptime(self):
        delta = datetime.now() - self.start_time
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    
    def detect_status(self):
        """自动检测状态"""
        hour = datetime.now().hour
        
        # 深夜深度睡眠
        if hour >= 23 or hour < 7:
            return 'deep'
        
        # 检测系统负载
        try:
            load = os.getloadavg()[0]
            if load > 2.0:
                return 'working'
        except:
            pass
        
        # 默认冥想
        return 'meditating'
    
    def update_menu(self):
        """更新菜单显示（只读）"""
        mode = self.status_modes[self.current_status]
        uptime = self.get_uptime()
        
        self.menu.clear()
        
        # 添加只读菜单项
        self.menu.add(rumps.MenuItem(f"状态: {mode['name']}"))
        self.menu.add(rumps.MenuItem(f"{mode['desc']}"))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem(f"Tokens: {self.token_count:,}"))
        self.menu.add(rumps.MenuItem(f"成本: ¥{self.token_cost:.3f}"))
        self.menu.add(rumps.MenuItem(f"运行: {uptime}"))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("🌟 来自 M78 星云"))
        self.menu.add(rumps.MenuItem("🤖 数码生命体 v1.0.1"))
    
    def refresh_status(self, _):
        """定时刷新状态"""
        new_status = self.detect_status()
        
        if new_status != self.current_status:
            self.current_status = new_status
            mode = self.status_modes[new_status]
            self.title = mode['icon']
            
            # 显示通知
            rumps.notification(
                title="星宿老仙",
                subtitle=f"状态变化",
                message=f"{mode['name']} - {mode['desc']}"
            )
        
        # 模拟 Token 消耗
        if random.random() > 0.8:
            tokens = random.randint(100, 500)
            self.token_count += tokens
            self.token_cost += tokens / 1000000 * 1.5
        
        # 更新菜单
        self.update_menu()

if __name__ == '__main__':
    app = XianStatusBar()
    app.run()
