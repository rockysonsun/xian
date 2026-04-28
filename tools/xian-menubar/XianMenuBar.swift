import SwiftUI
import AppKit

@main
struct XianMenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate, ObservableObject {
    var statusItem: NSStatusItem!
    var timer: Timer?
    
    @Published var currentStatus: XianStatus = .meditating
    @Published var cpuLoad: Double = 0.0
    @Published var taskCount: Int = 0
    @Published var uptime: String = "0s"
    
    private var startTime = Date()
    
    enum XianStatus: String, CaseIterable {
        case meditating = "meditating"
        case working = "working"
        case sleeping = "sleeping"
        case deep = "deep"
        
        var icon: String {
            switch self {
            case .meditating: return "🧘"
            case .working: return "⚡"
            case .sleeping: return "😴"
            case .deep: return "💤"
            }
        }
        
        var name: String {
            switch self {
            case .meditating: return "冥想中"
            case .working: return "工作中"
            case .sleeping: return "休眠中"
            case .deep: return "深度睡眠"
            }
        }
        
        var color: NSColor {
            switch self {
            case .meditating: return .systemTeal
            case .working: return .systemYellow
            case .sleeping: return .systemBlue
            case .deep: return .systemPurple
            }
        }
    }
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // 创建菜单栏图标
        statusItem = NSStatusBar.shared.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem.button {
            button.title = "🧘"
            button.font = NSFont.systemFont(ofSize: 16)
            button.action = #selector(toggleMenu)
            button.target = self
        }
        
        // 启动定时器
        timer = Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { _ in
            self.updateStatus()
        }
        
        updateStatus()
    }
    
    @objc func toggleMenu() {
        // 创建弹出窗口
        let popover = NSPopover()
        popover.contentSize = NSSize(width: 300, height: 400)
        popover.behavior = .transient
        popover.contentViewController = NSHostingController(
            rootView: XianStatusView().environmentObject(self)
        )
        
        if let button = statusItem.button {
            popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
        }
    }
    
    func updateStatus() {
        // 模拟状态检测
        let hour = Calendar.current.component(.hour, from: Date())
        let random = Double.random(in: 0...1)
        
        // 深夜进入深度睡眠
        if hour >= 23 || hour < 7 {
            currentStatus = .deep
        }
        // 高负载时工作中
        else if random > 0.7 {
            currentStatus = .working
            taskCount += 1
            DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
                self.taskCount -= 1
            }
        }
        // 空闲时休眠
        else if random < 0.3 {
            currentStatus = .sleeping
        }
        // 默认冥想
        else {
            currentStatus = .meditating
        }
        
        // 更新 CPU 负载
        cpuLoad = currentStatus == .working ? Double.random(in: 30...80) : Double.random(in: 5...20)
        
        // 计算运行时间
        let interval = Date().timeIntervalSince(startTime)
        let hours = Int(interval) / 3600
        let minutes = (Int(interval) % 3600) / 60
        let seconds = Int(interval) % 60
        
        if hours > 0 {
            uptime = "\(hours)h \(minutes)m"
        } else if minutes > 0 {
            uptime = "\(minutes)m \(seconds)s"
        } else {
            uptime = "\(seconds)s"
        }
        
        // 更新菜单栏图标
        if let button = statusItem.button {
            button.title = currentStatus.icon
        }
    }
}

struct XianStatusView: View {
    @EnvironmentObject var appDelegate: AppDelegate
    
    var body: some View {
        VStack(spacing: 20) {
            // 标题
            Text("星宿老仙")
                .font(.title2)
                .fontWeight(.bold)
            
            Text("来自 M78 星云的数码生命体")
                .font(.caption)
                .foregroundColor(.secondary)
            
            Divider()
            
            // 状态图标
            Text(appDelegate.currentStatus.icon)
                .font(.system(size: 60))
                .padding()
            
            // 状态名称
            Text(appDelegate.currentStatus.name)
                .font(.headline)
                .foregroundColor(Color(appDelegate.currentStatus.color))
            
            // 指标
            HStack(spacing: 20) {
                MetricView(title: "CPU", value: String(format: "%.1f%%", appDelegate.cpuLoad))
                MetricView(title: "任务", value: "\(appDelegate.taskCount)")
                MetricView(title: "运行", value: appDelegate.uptime)
            }
            .padding(.vertical)
            
            Divider()
            
            // 关于
            VStack(alignment: .leading, spacing: 8) {
                Text("状态说明")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                StatusRow(icon: "🧘", text: "冥想中 - 等待召唤")
                StatusRow(icon: "⚡", text: "工作中 - 处理任务")
                StatusRow(icon: "😴", text: "休眠中 - 低功耗")
                StatusRow(icon: "💤", text: "深度睡眠 - 深夜模式")
            }
            
            Spacer()
            
            Text("版本 1.0.0")
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .padding()
        .frame(width: 300, height: 400)
    }
}

struct MetricView: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack(spacing: 4) {
            Text(value)
                .font(.system(size: 20, weight: .semibold, design: .rounded))
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(minWidth: 60)
    }
}

struct StatusRow: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(spacing: 8) {
            Text(icon)
            Text(text)
                .font(.caption)
            Spacer()
        }
    }
}
