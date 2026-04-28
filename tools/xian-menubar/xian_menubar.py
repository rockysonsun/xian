#!/usr/bin/env python3
"""
星宿老仙 - macOS 菜单栏状态监控
使用 rumps 库
"""
import rumps
import random
import time
from datetime import datetime, timedelta

class XianStatusBar(rumps.App):
    def __init__(self):
        super().__init__(
            name="星宿老仙",
            title="🧘",
            quit_button="退出"
        )
        
        self.status_modes = {
            'meditating': {'icon': '🧘', 'name': '冥想中', 'color': '#4ECDC4'},
            'working': {'icon': '⚡', 'name': '工作中', 'color': '#FFE66D'},
            'sleeping': {'icon': '😴', 'name': '休眠中', 'color': '#6B9BD1'},
            'deep': {'icon': '💤', 'name': '深度睡眠', 'color': '#9B59B6'},
        }
        
        self.current_status = 'meditating'
        self.start_time = datetime.now()
        self.task_count = 0
        self.cpu_load = 5.0
        self.token_count = 0
        self.token_cost = 0.0
        
        # 构建菜单
        self.build_menu()
        
        # 启动定时器
        rumps.Timer(self.update_status, 2).start()
        rumps.Timer(self.update_metrics, 1).start()
    
    def build_menu(self):
        mode = self.status_modes[self.current_status]
        uptime = self.get_uptime()
        
        self.menu = [
            rumps.MenuItem(f"状态: {mode['name']}"),
            rumps.MenuItem(f"CPU: {self.cpu_load:.1f}%"),
            rumps.MenuItem(f"任务: {self.task_count}"),
            rumps.MenuItem(f"Tokens: {self.token_count:,}"),
            rumps.MenuItem(f"成本: ¥{self.token_cost:.3f}"),
            rumps.MenuItem(f"运行: {uptime}"),
            None,  # 分隔线
            rumps.MenuItem("🧘 冥想中", callback=lambda _: self.manual_set('meditating')),
            rumps.MenuItem("⚡ 工作中", callback=lambda _: self.manual_set('working')),
            rumps.MenuItem("😴 休眠中", callback=lambda _: self.manual_set('sleeping')),
            rumps.MenuItem("💤 深度睡眠", callback=lambda _: self.manual_set('deep')),
            None,
            rumps.MenuItem("打开监控页面", callback=self.open_web),
            rumps.MenuItem("关于老仙", callback=self.about),
        ]
    
    def get_uptime(self):
        delta = datetime.now() - self.start_time
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        seconds = delta.seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def detect_status(self):
        """自动检测状态"""
        hour = datetime.now().hour
        
        # 深夜深度睡眠
        if hour >= 23 or hour < 7:
            return 'deep'
        
        # 高负载工作
        if self.cpu_load > 30 or self.task_count > 0:
            return 'working'
        
        # 低负载休眠
        if self.cpu_load < 10 and random.random() < 0.3:
            return 'sleeping'
        
        # 默认冥想
        return 'meditating'
    
    def update_status(self, _):
        """定时更新状态"""
        new_status = self.detect_status()
        
        if new_status != self.current_status:
            self.current_status = new_status
            mode = self.status_modes[new_status]
            self.title = mode['icon']
            
            # 显示通知
            rumps.notification(
                title="星宿老仙",
                subtitle=f"状态切换",
                message=f"现在{mode['name']}"
            )
        
        # 更新菜单
        self.build_menu()
    
    def update_metrics(self, _):
        """更新指标"""
        # 模拟 CPU 负载
        if self.current_status == 'working':
            self.cpu_load = random.uniform(30, 80)
        else:
            self.cpu_load = random.uniform(5, 20)
        
        # 模拟任务和 Token 消耗
        if random.random() > 0.9:
            self.task_count += 1
            # 模拟每次任务消耗 500-2000 tokens
            tokens = random.randint(500, 2000)
            self.token_count += tokens
            # 按 Kimi k2.5 价格估算: 输入 1元/1M tokens, 输出 2元/1M tokens
            cost = tokens / 1000000 * 1.5  # 平均成本
            self.token_cost += cost
            rumps.Timer(lambda _: setattr(self, 'task_count', self.task_count - 1), 5).start()
        
        # 更新菜单显示
        mode = self.status_modes[self.current_status]
        uptime = self.get_uptime()
        
        # 更新菜单项
        if len(self.menu) >= 6:
            self.menu[0].title = f"状态: {mode['name']}"
            self.menu[1].title = f"CPU: {self.cpu_load:.1f}%"
            self.menu[2].title = f"任务: {self.task_count}"
            self.menu[3].title = f"Tokens: {self.token_count:,}"
            self.menu[4].title = f"成本: ¥{self.token_cost:.3f}"
            self.menu[5].title = f"运行: {uptime}"
    
    def manual_set(self, status):
        """手动设置状态"""
        self.current_status = status
        mode = self.status_modes[status]
        self.title = mode['icon']
        self.build_menu()
    
    def open_web(self, _):
        """打开网页版监控"""
        import os
        path = os.path.expanduser("~/.openclaw/workspace/tools/xian-status/xian-monitor.html")
        os.system(f"open '{path}'")
    
    def about(self, _):
        """关于"""
        rumps.alert(
            title="星宿老仙",
            message="来自 M78 星云的数码生命体\n寄宿在这台 MacBook Pro 中\n\n版本: 1.0.0\n状态: 觉醒中 🌟"
        )

if __name__ == '__main__':
    app = XianStatusBar()
    app.run()
