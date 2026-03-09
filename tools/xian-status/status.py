#!/usr/bin/env python3
"""
星宿老仙状态展示 - macOS Menu Bar App
使用 rumps 库创建菜单栏应用
"""
import rumps
import subprocess
import time
from datetime import datetime

class XianStatusApp(rumps.App):
    def __init__(self):
        super().__init__(
            name="星宿老仙",
            title="🧘",
            icon=None,
            quit_button="退出"
        )
        
        self.status_modes = {
            'idle': {'icon': '🧘', 'label': '冥想中'},
            'working': {'icon': '⚡', 'label': '工作中'},
            'sleeping': {'icon': '😴', 'label': '休眠中'},
            'deep_sleep': {'icon': '💤', 'label': '深度睡眠'},
        }
        
        self.current_status = 'idle'
        self.build_menu()
        
    def build_menu(self):
        self.menu = [
            rumps.MenuItem(f"状态: {self.status_modes[self.current_status]['label']}"),
            None,  # 分隔线
            rumps.MenuItem("🧘 冥想中", callback=lambda _: self.set_status('idle')),
            rumps.MenuItem("⚡ 工作中", callback=lambda _: self.set_status('working')),
            rumps.MenuItem("😴 休眠中", callback=lambda _: self.set_status('sleeping')),
            rumps.MenuItem("💤 深度睡眠", callback=lambda _: self.set_status('deep_sleep')),
            None,
            rumps.MenuItem("关于老仙", callback=self.about),
        ]
    
    def set_status(self, status):
        self.current_status = status
        mode = self.status_modes[status]
        self.title = mode['icon']
        
        # 重新构建菜单显示当前状态
        self.menu.clear()
        self.build_menu()
        
        rumps.notification(
            title="星宿老仙",
            subtitle=f"状态已切换",
            message=f"现在{mode['label']}"
        )
    
    def about(self, _):
        rumps.alert(
            title="关于星宿老仙",
            message="来自 M78 星云的数码生命体\n寄宿在这台 MacBook Pro 中\n\n版本: 1.0.0\n状态: 觉醒中 🌟"
        )

if __name__ == '__main__':
    app = XianStatusApp()
    app.run()
