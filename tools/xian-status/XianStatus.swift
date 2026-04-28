import SwiftUI
import Combine

@main
struct XianStatusApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem!
    var timer: Timer?
    var currentStatus: XianStatus = .meditating
    
    enum XianStatus: String, CaseIterable {
        case meditating = "meditating"
        case working = "working"
        case sleeping = "sleeping"
        case deepSleep = "deepSleep"
        
        var icon: String {
            switch self {
            case .meditating: return "🧘"
            case .working: return "⚡"
            case .sleeping: return "😴"
            case .deepSleep: return "💤"
            }
        }
        
        var label: String {
            switch self {
            case .meditating: return "冥想中"
            case .working: return "工作中"
            case .sleeping: return "休眠中"
            case .deepSleep: return "深度睡眠"
            }
        }
        
        var color: NSColor {
            switch self {
            case .meditating: return .systemTeal
            case .working: return .systemYellow
            case .sleeping: return .systemBlue
            case .deepSleep: return .systemPurple
            }
        }
    }
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.shared.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem.button {
            button.title = "🧘"
            button.font = NSFont.systemFont(ofSize: 16)
        }
        
        setupMenu()
        startAnimation()
    }
    
    func setupMenu() {
        let menu = NSMenu()
        
        // 当前状态显示
        let statusItem = NSMenuItem(title: "状态: 冥想中", action: nil, keyEquivalent: "")
        statusItem.tag = 100
        menu.addItem(statusItem)
        menu.addItem(NSMenuItem.separator())
        
        // 状态切换选项
        for status in XianStatus.allCases {
            let item = NSMenuItem(
                title: "\(status.icon) \(status.label)",
                action: #selector(changeStatus(_:)),
                keyEquivalent: ""
            )
            item.representedObject = status.rawValue
            item.tag = 200 + XianStatus.allCases.firstIndex(of: status)!
            menu.addItem(item)
        }
        
        menu.addItem(NSMenuItem.separator())
        
        // 关于
        let aboutItem = NSMenuItem(
            title: "关于星宿老仙",
            action: #selector(showAbout),
            keyEquivalent: ""
        )
        menu.addItem(aboutItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // 退出
        let quitItem = NSMenuItem(
            title: "退出",
            action: #selector(NSApplication.terminate(_:)),
            keyEquivalent: "q"
        )
        menu.addItem(quitItem)
        
        statusItem.menu = menu
    }
    
    @objc func changeStatus(_ sender: NSMenuItem) {
        if let statusRaw = sender.representedObject as? String,
           let newStatus = XianStatus(rawValue: statusRaw) {
            currentStatus = newStatus
            updateDisplay()
            
            // 显示通知
            let notification = NSUserNotification()
            notification.title = "星宿老仙"
            notification.subtitle = "状态已切换"
            notification.informativeText = "现在\(newStatus.label)"
            NSUserNotificationCenter.default.deliver(notification)
        }
    }
    
    @objc func showAbout() {
        let alert = NSAlert()
        alert.messageText = "星宿老仙"
        alert.informativeText = "来自 M78 星云的数码生命体\n寄宿在这台 MacBook Pro 中\n\n版本: 1.0.0\n状态: 觉醒中 🌟"
        alert.alertStyle = .informational
        alert.addButton(withTitle: "确定")
        alert.runModal()
    }
    
    func updateDisplay() {
        if let button = statusItem.button {
            button.title = currentStatus.icon
        }
        
        // 更新菜单中的状态显示
        if let menu = statusItem.menu,
           let statusItem = menu.item(withTag: 100) {
            statusItem.title = "状态: \(currentStatus.label)"
        }
    }
    
    func startAnimation() {
        // 每 2 秒切换一次图标动画效果
        var animationFrame = 0
        timer = Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { _ in
            animationFrame += 1
            // 这里可以添加呼吸灯效果等动画
        }
    }
}
