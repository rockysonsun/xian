# KCP 通信协议学习笔记

> 学习时间: 2026-03-19
> 官方仓库: https://github.com/skywind3000/kcp
> 协议定位: 快速可靠的 ARQ (Automatic Repeat reQuest) 协议

---

## 一、KCP 是什么

KCP 是一个**快速可靠协议**，以比 TCP 浪费 **10%-20% 带宽**的代价，换取：
- 平均延迟降低 **30%-40%**
- 最大延迟降低 **三倍**

### 核心特点
| 特性 | 说明 |
|-----|-----|
| **纯算法实现** | 不负责底层收发，需使用者定义 UDP 收发方式 |
| **零系统调用** | 连时钟都需要外部传入，内部无任何系统调用 |
| **极简代码** | 仅 `ikcp.h` + `ikcp.c` 两个文件 |
| **易集成** | 拷贝两个文件到项目，写几行代码即可使用 |

### 设计哲学对比
| 维度 | TCP | KCP |
|-----|-----|-----|
| **设计目标** | 流量最大化(每秒传输多少KB) | 流速最大化(单包传输耗时) |
| **比喻** | 流速慢但流量大的大运河 | 水流湍急的小激流 |
| **适用场景** | 文件传输、网页浏览 | 实时游戏、视频通话、直播推流 |

---

## 二、KCP vs TCP 核心差异

### 2.1 RTO (重传超时) 计算
```
TCP:  RTO × 2  (连续丢3次包 → RTO×8，非常恐怖)
KCP:  RTO × 1.5 (快速模式下，实验证明1.5是较好值)
```

### 2.2 重传策略
| 协议 | 策略 | 说明 |
|-----|-----|-----|
| TCP | 全部重传 | 丢包后重传从丢包开始的所有数据 |
| KCP | 选择性重传 | 只重传真正丢失的数据包 |

### 2.3 快速重传机制
```
发送端发送: 1, 2, 3, 4, 5
收到ACK:    1, 3, 4, 5

TCP: 等超时后才重传2
KCP: 收到ACK3(跳过1次)→收到ACK4(跳过2次)→立即重传2，无需等待超时
```

### 2.4 ACK 延迟
| 协议 | 行为 | 影响 |
|-----|-----|-----|
| TCP | 延迟发送ACK (即使NODELAY也无效) | 算出较大RTT，延长丢包判断 |
| KCP | ACK是否延迟可配置 | 更精确的RTT计算 |

### 2.5 ARQ 响应模型
| 模型 | 含义 | 问题 |
|-----|-----|-----|
| UNA | 此编号前所有包已收到 | 光用UNA导致全部重传 |
| ACK | 该编号包已收到 | 光用ACK丢失成本高 |
| **KCP** | **ACK + UNA** | 除单独ACK包外，所有包都带UNA信息 |

### 2.6 流控策略
| 模式 | 说明 |
|-----|-----|
| 正常模式 | 同TCP公平退让法则 (发送缓存 + 接收缓存 + 丢包退让 + 慢启动) |
| 快速模式 | 跳过丢包退让和慢启动，仅用前两项控制发送频率 |
| **代价** | 牺牲部分公平性和带宽利用率，换取开着BT都能流畅传输 |

---

## 三、基本使用流程

### 3.1 创建 KCP 对象
```cpp
// conv: 会话编号，通信双方需保持一致
// user: 给回调函数的指针，用于区分多个KCP对象
ikcpcb *kcp = ikcp_create(conv, user);
```

### 3.2 设置回调函数 (底层输出)
```cpp
// KCP需要发送数据时调用此函数
int udp_output(const char *buf, int len, ikcpcb *kcp, void *user)
{
    // 调用UDP发送
    return udp_send(buf, len);
}

kcp->output = udp_output;
```

### 3.3 循环调用 update
```cpp
// 定期调用更新KCP状态，传入当前时钟(毫秒)
ikcp_update(kcp, millisec);

// 或使用 ikcp_check 优化调用频率
IUINT32 next = ikcp_check(kcp, current_time);
// next 告诉你下次需要调用 update 的时间
```

### 3.4 输入下层数据包
```cpp
// 收到UDP包时调用
ikcp_input(kcp, received_udp_packet, received_udp_size);
```

### 3.5 发送/接收数据
```cpp
// 发送数据
ikcp_send(kcp, data, size);

// 接收数据
int len = ikcp_recv(kcp, buffer, buffer_size);
```

---

## 四、协议配置

### 4.1 工作模式配置
```cpp
int ikcp_nodelay(ikcpcb *kcp, int nodelay, int interval, int resend, int nc);
```

| 参数 | 说明 |
|-----|-----|
| `nodelay` | 0=不启用nodelay模式, 1=启用 |
| `interval` | 内部工作间隔(毫秒)，如10ms或20ms |
| `resend` | 快速重传模式，0=关闭，2=2次ACK跨越直接重传 |
| `nc` | 是否关闭流控，0=不关闭，1=关闭 |

**配置示例**:
```cpp
// 普通模式
ikcp_nodelay(kcp, 0, 40, 0, 0);

// 极速模式 (游戏、实时通信推荐)
ikcp_nodelay(kcp, 1, 10, 2, 1);
```

### 4.2 窗口大小配置
```cpp
int ikcp_wndsize(ikcpcb *kcp, int sndwnd, int rcvwnd);
```
- 默认窗口大小: 32 (单位是包，不是字节)
- 类似 TCP 的 SND_BUF 和 RCV_BUF

### 4.3 MTU 设置
```cpp
ikcp_setmtu(kcp, mtu);
```
- 默认 MTU: 1400 字节
- 影响数据包归并及分片的最大传输单元

### 4.4 最小 RTO 设置
```cpp
kcp->rx_minrto = 10;  // 快速模式下默认30ms，可手动改更小
```

---

## 五、最佳实践

### 5.1 内存分配器接管
```cpp
// 自定义内存分配
ikcp_allocator(my_new_malloc, my_new_free);
// 注意：要在创建KCP对象前设置
```

### 5.2 大规模连接优化 (>3000个)
使用 `ikcp_check` 减少 `ikcp_update` 调用次数：
```cpp
// 不用每10ms对每个连接调用update
// 用check获取下次需要update的时间
IUINT32 next_time = ikcp_check(kcp, current);
// 将连接按next_time排序，只处理到期的
```

### 5.3 混合可靠/非可靠传输
```cpp
// channel 0: KCP可靠传输
// channel 1: UDP非可靠传输
// channel 2: TCP大文件传输

if (channel == 0) {
    ikcp_send(kcp, data, len);
} else if (channel == 1) {
    udp_send(data, len);
}
```

### 5.4 前向纠错 (FEC) 注意事项
- 下层使用FEC时，相同原始数据包**不要两次input到KCP**
- 需记录已input的包，避免重复ack浪费带宽

---

## 六、开源生态

| 项目 | 语言 | 说明 |
|-----|-----|-----|
| [kcptun](https://github.com/xtaci/kcptun) | Go | 高速远程端口转发隧道 |
| [kcp-go](https://github.com/xtaci/kcp-go) | Go | 高安全性Go实现 |
| [kcp-java](https://github.com/hkspirt/kcp-java) | Java | Java版本 |
| [kcp-netty](https://github.com/szhnet/kcp-netty) | Java | 基于Netty |
| [kcp-csharp](https://github.com/limpo1989/kcp-csharp) | C# | C#移植版 |
| [kcp-rs](https://github.com/en/kcp-rs) | Rust | Rust移植版 |
| [node-kcp](https://github.com/leenjewel/node-kcp) | Node.js | Node.js绑定 |
| [pykcp](https://github.com/enkiller/pykcp) | Python | Python版本 |

### 知名应用
- [原神](https://ys.mihoyo.com/) - 游戏消息传输加速
- [v2ray](https://www.v2ray.com) - 代理软件集成
- [frp](https://github.com/fatedier/frp) - 内网穿透
- [shadowsocks-android](https://github.com/shadowsocks/shadowsocks-android) - 集成kcptun
- [Lantern](https://getlantern.org/) - VPN加速

---

## 七、适用场景总结

| 场景 | 是否推荐 | 原因 |
|-----|---------|-----|
| 实时游戏 | ✅ 强烈推荐 | 低延迟是关键 |
| 视频直播/推流 | ✅ 推荐 | 流畅性优先 |
| 语音通话 | ✅ 推荐 | 实时性要求高 |
| 文件传输 | ⚠️ 一般 | TCP更充分利用带宽 |
| 网页浏览 | ❌ 不推荐 | 不需要极低延迟 |
| 大规模数据传输 | ❌ 不推荐 | 10-20%带宽浪费 |

---

## 八、核心口诀

```
KCP 快，TCP 稳
带宽换延迟，实时场景神
两文件，易集成
UDP 底下跑，流速赛火箭
```

---

*学习完毕，随时待命解答问题！* 🐉
