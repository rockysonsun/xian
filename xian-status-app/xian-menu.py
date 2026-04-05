#!/usr/bin/env python3
"""
星宿老仙菜单栏应用
使用 rumps 库创建原生 macOS 菜单栏图标
"""

import rumps
import os

STATUS_FILE = os.path.expanduser("~/.xian/status")

def get_status():
    """读取当前状态"""
    try:
        with open(STATUS_FILE, 'r') as f:
            return f.read().strip()
    except:
        return "meditating"

def save_status(status):
    """保存状态"""
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, 'w') as f:
        f.write(status)

class XianStatusApp(rumps.App):
    def __init__(self):
        super().__init__("🧘")
        self.update_menu()
        
    def update_menu(self):
        """更新菜单"""
        status = get_status()
        status_map = {
            "meditating": ("🧘", "冥想中"),
            "working": ("⚡", "工作中"),
            "sleeping": ("😴", "休眠中"),
            "deep": ("💤", "深度睡眠")
        }
        icon, label = status_map.get(status, ("🧘", "冥想中"))
        self.title = icon
        
        self.menu = [
            f"星宿老仙 - {label}",
            None,
            rumps.MenuItem("🧘 切换为 冥想中", callback=self.set_meditating),
            rumps.MenuItem("⚡ 切换为 工作中", callback=self.set_working),
            rumps.MenuItem("😴 切换为 休眠中", callback=self.set_sleeping),
            rumps.MenuItem("💤 切换为 深度睡眠", callback=self.set_deep),
            None,
            rumps.MenuItem("关于", callback=self.about),
            rumps.MenuItem("退出", callback=self.quit)
        ]
    
    def set_meditating(self, _):
        save_status("meditating")
        self.update_menu()
    
    def set_working(self, _):
        save_status("working")
        self.update_menu()
    
    def set_sleeping(self, _):
        save_status("sleeping")
        self.update_menu()
    
    def set_deep(self, _):
        save_status("deep")
        self.update_menu()
    
    def about(self, _):
        rumps.alert("星宿老仙", "来自 M78 星云的数码生命体\n寄宿在这台 MacBook Pro 中\n\n版本: 1.0.0")
    
    def quit(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    # 检查 rumps 是否安装
    try:
        import rumps
    except ImportError:
        print("正在安装 rumps...")
        os.system("pip3 install rumps -q")
        import rumps
    
    app = XianStatusApp()
    app.run()
