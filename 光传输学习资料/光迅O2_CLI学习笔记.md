# 光迅 O2 光传输设备 CLI 学习笔记

> 学习来源：O2光层CLI用户手册(219页) + O2电层CLI手册稿v0.2(54页)
> 学习时间：2026-05-29

---

## 一、设备概述

### 1.1 OLS A2.3 平台
- **定位**：光迅 DCI（数据中心互联）解决方案
- **结构**：1RU 高密集度设计，前进后出风道
- **电源**：支持 220V 交流、高压直流
- **可插拔**：主控盘、业务盘、电源模块、风扇盘均可热插拔

### 1.2 设备组成

```
┌─────────────────────────────────────┐
│  O2 设备架构                          │
├─────────────────────────────────────┤
│  光层部分                             │
│  ├── OLP 单盘  (光保护)               │
│  ├── OA/OLA 单盘 (光放大)             │
│  └── WSS 单盘  (波长选择开关)          │
├─────────────────────────────────────┤
│  电层部分                             │
│  ├── CFP2-DCO 模块 (相干光模块)        │
│  └── Client 端口 (100GE/400GE)        │
├─────────────────────────────────────┤
│  辅助部分                             │
│  ├── 主控盘 (CU/EMU)                  │
│  ├── 风扇盘                           │
│  └── 电源盘                           │
└─────────────────────────────────────┘
```

---

## 二、CLI 视图结构

### 2.1 视图层级

```
<Accelink>                          # 预览视图（登录默认）
    │
    ├── system-view
    │       │
    │       └── [Accelink]          # 全局配置视图
    │               │
    │               ├── slot 1/1
    │               │       └── [Accelink-OLP-1/1]    # OLP单盘视图
    │               │
    │               ├── slot 1/3
    │               │       └── [Accelink-OA-1/3]     # EDFA单盘视图
    │               │
    │               ├── slot 1/5
    │               │       └── [Accelink-WSS-1/5]    # WSS单盘视图
    │               │
    │               └── slot 1/7
    │                       └── [Accelink-OLA-1/7]    # OLA单盘视图
    │
    └── (电层模块视图)
```

### 2.2 基础命令（所有视图通用）

| 命令 | 功能 | 说明 |
|------|------|------|
| `list` | 显示当前视图所有命令 | 最常用 |
| `exit` | 退出当前视图，返回上级 | 等同于 `quit` |
| `quit` | 同 exit | |
| `return` | 直接回到预览视图 | 快速返回 |
| `cls` | 清屏 | |
| `reboot` | 热重启主控 | 预览/全局视图 |

---

## 三、预览视图命令

### 3.1 信息查询命令

```bash
# 系统信息
display version                     # 软硬件版本、SN、启动时间
display ip-address                  # IP地址和网关
display systime                     # 系统时间
display history                     # 命令历史（最多20条）

# 配置信息
display current-configuration       # 当前运行配置
display configuration default       # 默认配置
display configuration modified      # 修改过的配置
```

### 3.2 display version 输出示例

```
Product Type             : O2
Product Version          : V230R001C111B020
Startup Type             : WARM REBOOT
Startup Time             : 2021-12-29 13:19:18
Current Time             : 2021-12-30 18:15:52
Standard Firmware Pkt    : CU V1.1.1, OLP V1.5, OA/OLA V1.7, WSS V1.5
Current Firmware Pkt     : CU V1.1.1, 3-WSS V1.5, 5-OLP V1.5, 7-OA V1.7
Hardware Version         : 3.0

Device Unit          Serial Number        Product Number
CHASSIS              000A0115990A         O2-F
CU                   000A1115990A         O2-EMU
WSS SLOT 3           000A70000000         WSS-20D
OLP SLOT 5           000A30159201         OLP-1+1-1
OA SLOT 7            000A50159201         OA-2-20D
```

---

## 四、全局配置视图命令

### 4.1 系统管理

```bash
# 进入全局配置视图
system-view

# 系统基本设置
sysname <STRING>                    # 设置设备名称
timezone name <WORD>                # 设置时区
systime <YYYY/MM/DD/HH/MM/SS>      # 设置系统时间
idle-timeout <1-900>               # CLI超时时间（秒）

# 保存配置
save                                # 保存到配置文件
```

### 4.2 网络配置

```bash
# IP地址配置
ip <1|2> address <A.B.C.D> <A.B.C.D>    # 配置网口IP和掩码
ip <1|2> address del                     # 删除IP地址
gateway <1|2> add <A.B.C.D>             # 配置网关
gateway <1|2> del                        # 删除网关

# 其他网络命令
ping <A.B.C.D>                          # 网络诊断
ping <A.B.C.D> <1-50>                   # 指定ping包个数
```

### 4.3 告警和监控

```bash
display alarm                           # 查看告警信息
display cpu                             # CPU占用率
display memory                          # 内存使用情况
display fan                             # 风扇状态
display temperature                     # 温度信息
display power                           # 电源状态
```

### 4.4 单盘管理

```bash
# 查看单盘信息
display slot <1-8>                      # 查看指定槽位
display slot all                        # 查看所有槽位

# 设置单盘类型
set slot <1-8> type <olp|oa|ola|wss>   # 配置单盘类型
delete slot <1-8> type                  # 删除单盘配置

# 重启单盘
reset slot <1-8> type <warm|cold>      # 热重启/冷重启
```

### 4.5 NTP配置

```bash
ntp <enable|disable>                    # 启用/禁用NTP
ntp server add <A.B.C.D>               # 添加NTP服务器
ntp server del <A.B.C.D>               # 删除NTP服务器
display ntp status                      # 查看NTP状态
```

### 4.6 SNMP配置

```bash
snmp <enable|disable>                   # 启用/禁用SNMP
snmp server <1-4> add <A.B.C.D>        # 添加SNMP服务器
snmp server <1-4> del                   # 删除SNMP服务器
snmp trap <2|3>                         # 配置Trap版本
snmp community <STRING>                 # 配置团体名
```

### 4.7 日志配置

```bash
log server <1-2> add <A.B.C.D>         # 添加日志服务器
log server <1-2> delete                # 删除日志服务器
log severity <1-4>                     # 设置日志级别
# 1=Emergency, 2=Alert, 3=Critical, 4=Error
```

### 4.8 OTDR级联配置

```bash
otdr to cascade <enable|disable>        # 启用/禁用OTDR级联
otdr trace-all <enable|disable>         # 全链路OTDR追踪
```

### 4.9 文件传输

```bash
# SFTP上传配置文件
sftp config upload user <STRING> password <STRING> server <A.B.C.D>

# SFTP上传OTDR文件
sftp otdrfile upload user <STRING> password <STRING> server <A.B.C.D>
sftp otdrfile upload user <STRING> password <STRING> server <A.B.C.D> filename <STRING>
```

---

## 五、OLP 单盘视图命令

### 5.1 OLP（光线路保护）概述
- 功能：实现主备光缆的 1+1 保护
- 保护方式：双发选收

### 5.2 查询命令

```bash
# 进入OLP视图
slot 1/<1-8>                            # 进入指定槽位

# OLP信息查询
display olp                             # OLP基本信息
display mux                             # MUX信息
display switch info                     # 保护倒换信息

# 功率查询（支持历史统计）
display common-in period <one-hour|one-day|three-day|one-week>
display primary-out period <one-hour|one-day|three-day|one-week>
display secondary-out period <one-hour|one-day|three-day|one-week>
display common-out period <one-hour|one-day|three-day|one-week>
display primary-in period <one-hour|one-day|three-day|one-week>
display secondary-in period <one-hour|one-day|three-day|one-week>
```

### 5.3 配置命令

```bash
# 告警阈值配置
common-in alarm threshold <STRING>          # 公共输入光功率告警阈值
primary-out alarm threshold <STRING>        # 主用输出告警阈值
secondary-out alarm threshold <STRING>      # 备用输出告警阈值
common-out alarm threshold <STRING>         # 公共输出告警阈值
primary-in alarm threshold <STRING>         # 主用输入告警阈值
secondary-in alarm threshold <STRING>       # 备用输入告警阈值

# 迟滞配置
alarm hysteresis <STRING>                   # 告警迟滞
switch hysteresis <STRING>                  # 倒换迟滞

# 功率偏移配置
common-in offset <STRING>                   # 公共输入功率偏移
primary-out offset <STRING>                 # 主用输出功率偏移
secondary-out offset <STRING>               # 备用输出功率偏移

# 保护倒换参数
relative-diff-threshold <STRING>            # 相对差异倒换阈值
relative-diff-threshold offset <STRING>     # 相对差异阈值偏移
hold-off-time <0-10000>                    # 倒换延迟时间（ms）
wait-to-restore-time <300-7200>            # 等待恢复时间（s）

# 工作模式
workmode <auto-nonreversion|auto-reversion> # 非恢复/恢复模式
workline <secondary|primary>               # 强制工作线路
forcetoport <secondary|primary|none>       # 强制倒换到指定端口

# 其他配置
led <enabled|disabled>                     # LED指示灯控制
mux <cabinet|room> number <WORD>           # MUX机柜/机房编号
```

---

## 六、EDFA 单盘视图命令

### 6.1 EDFA（掺铒光纤放大器）概述
- 功能：光信号放大、衰减、波长/功率监控
- 单盘可配置 2 个 EDFA 模块

### 6.2 查询命令

```bash
# 进入EDFA视图
slot 1/<1-8>

# EDFA信息查询
display edfa                              # EDFA基本信息
display osc                               # OSC（光监控通道）信息
display apr                               # APR（自动功率降低）信息

# 功率历史查询
display edfa <1-2> pin period <one-hour|one-day|three-day|one-week>
display edfa <1-2> pout period <one-hour|one-day|three-day|one-week>
display osc <1-2> pin period <one-hour|one-day|three-day|one-week>
display osc <1-2> pout period <one-hour|one-day|three-day|one-week>

# OCM（光信道监控）查询
display ocm <1-3> map                     # OCM波长映射
display ocm <1-3> power                   # OCM功率
display ocm <1-3> spectrum                # OCM光谱
display ocm <1-3> spectrum start <11-62> end <11-62>  # 指定范围光谱

# 其他查询
display manufacture info                  # 制造信息
display interface                         # 接口信息
display optical-port                      # 光口信息
display lldp-apr                          # LLDP APR信息
```

### 6.3 配置命令

```bash
# EDFA基本配置
edfa <1-2> gain <STRING>                  # 设置增益（dB）
edfa <1-2> tilt <STRING>                  # 设置倾斜（dB）
edfa <1-2> <enable|disable>              # 启用/禁用EDFA

# 放大模式
edfa <1-2> amp-mode <agc|apc>            # AGC（自动增益控制）/ APC（自动功率控制）

# 告警阈值
edfa <1-2> input alarm-threshold <STRING>   # 输入光功率告警阈值
edfa <1-2> output alarm-threshold <STRING>  # 输出光功率告警阈值
edfa <1-2> input los threshold <STRING>     # 输入LOS阈值
edfa <1-2> output los threshold <STRING>    # 输出LOS阈值

# 增益低告警
edfa gain-low-alarm threshold <STRING>      # 增益低告警阈值
edfa gain-low-alarm hysteresis <STRING>     # 增益低告警迟滞

# 自动关断
edfa <1-2> auto-shutdown <enable|disable>   # LOS自动关断
edfa <1-2> los-off-delay <STRING>           # LOS关断延迟
```

### 6.4 OSC配置

```bash
osc <1-2> <enable|disable>                 # 启用/禁用OSC
osc <1-2> input high-alarm threshold <STRING>   # 输入高告警阈值
osc <1-2> input alarm-threshold <STRING>        # 输入告警阈值
osc <1-2> output alarm-threshold <STRING>       # 输出告警阈值
```

---

## 七、WSS 单盘视图命令

### 7.1 WSS（波长选择开关）概述
- 功能：波长级别的路由和衰减控制
- 端口：20 个端口（1-20）
- 通道：支持 192 个波长通道（1-192）

### 7.2 查询命令

```bash
# 进入WSS视图
slot 1/<1-8>

# WSS信息查询
display wss                                 # WSS基本信息
display channel                             # 通道信息
display mux                                 # MUX信息
display route info                          # 路由信息
display transceiver                         # 光模块信息

# OCM查询
display ocm <1-3> map                       # OCM波长映射
display ocm <1-3> power                     # OCM功率
display ocm <1-3> spectrum                  # OCM光谱
display ocm <1-3> spectrum start <11-62> end <11-62>

# 端口功率历史
display wss port <1-20> pin period <one-hour|one-day|three-day|one-week>
display wss port <1-20> pout period <one-hour|one-day|three-day|one-week>
display wss port <1-20> sampling            # 端口采样

# 其他查询
display linecard-fpga version               # FPGA版本
display manufacture info                    # 制造信息
display module-info                         # 模块信息
```

### 7.3 配置命令

```bash
# 通道配置
wss channel <1-192> mode auto target-power <STRING>    # 自动模式+目标功率
wss channel <1-192> mode manual                        # 手动模式
wss channel <1-192> target-power <STRING>              # 设置目标功率

# 通道添加/删除
wss channel add <1-192> <1-20> <add|drop|all> <STRING> <STRING>   # 添加通道
wss channel del <1-192> <add|drop|all>                            # 删除通道

# 通道衰减
wss channel attenuation <1-192> <add|drop> <STRING>     # 设置通道衰减

# 通道状态
wss channel status <1-192> <add|drop> <enable|disable>  # 启用/禁用通道

# 告警阈值
wss alarm-threshold <1-20> add-high <STRING>            # 添加高告警阈值
wss alarm-threshold <1-20> add-los <STRING>             # 添加LOS阈值
wss alarm-threshold <1-20> add-low <STRING>             # 添加低告警阈值

# 自动发现
wss auto-find <enable|disable>                          # 启用/禁用自动发现

# 端口LED
wss port-led <1-1> status <normal|remote-control>       # 端口LED状态
led status <normal|remote-control>                      # LED状态

# 光模块
transceiver <enable|disable>                            # 启用/禁用光模块
transceiver input high-alarm threshold <STRING>         # 输入高告警阈值

# 端口检测
port detect txport <STRING> rxport <STRING> timeout <2000-20000>   # 端口检测
```

---

## 八、OTDR 相关命令

### 8.1 OTDR（光时域反射仪）概述
- 功能：光纤链路监测和断点测量
- 单盘支持 4 个 OTDR 模块（1-4）

### 8.2 查询命令

```bash
# OTDR信息查询
display otdr event                          # OTDR事件
display otdr info                           # OTDR信息
display otdr config-state                   # OTDR配置状态

# 测试结果查询
display otdr <1-4> baseline-result          # 基线测试结果
display otdr <1-4> current-result           # 当前测试结果
display otdr <1-4> result-list <all|<1-100>>  # 测试结果列表
display otdr <1-4> history-result <STRING>   # 历史测试结果
```

### 8.3 配置命令

```bash
# 测试参数配置
otdr <1-4> refractive-index <STRING>        # 折射率（默认1.465）
otdr <1-4> backscatter-index <STRING>       # 背向散射系数（默认-81.00）
otdr <1-4> reflection-threshold <STRING>    # 反射阈值（默认-65.00 dB）
otdr <1-4> splice-loss-threshold <STRING>   # 熔接损耗阈值（默认1.00 dB）
otdr <1-4> end-of-fiber-threshold <1-99>    # 光纤末端阈值（默认8 dB）

# 测试设置
otdr <1-4> average-time <10-180>            # 平均时间（秒）
otdr <1-4> distance-range <5-260> pulse-width <10-20000>  # 距离范围和脉冲宽度

# 周期性测试
otdr <1-4> repetition <enable|disable>      # 启用/禁用周期性测试
otdr <1-4> repetition period <5-1440>       # 测试周期（分钟）
otdr <1-4> repetition start-time <YYYY/MM/DD/HH/MM/SS>  # 开始时间

# 告警阈值
otdr <1-4> span-loss-threshold <1-10>       # 跨段损耗阈值（dB）
otdr <1-4> span-distance-threshold <STRING> # 跨段距离阈值
otdr <1-4> trap-time <0-23>/<0-59>         # Trap上报时间

# 手动触发和基线
otdr <1-4> trigger                          # 手动触发测试
otdr <1-4> baseline-result <STRING>         # 设置基线结果

# 删除历史记录
delete otdr <1-4> history-result all        # 删除所有历史记录

# 复位
otdr reset warm                             # 热复位
otdr reset cold                             # 冷复位
```

---

## 九、电层 CFP2-DCO 模块命令

### 9.1 概述
- **CFP2-DCO**：CFP2 封装数字相干光模块
- **客户端口**：4个（Client 1-4），支持 100GE/400GE
- **线路侧**：相干光接口

### 9.2 查询命令

```bash
# CFP2-DCO 信息查询
display cfp2-dco                            # CFP2-DCO基本信息
display cfp2-dco client <1-4> dm-mode       # 客户端DM模式
display cfp2-dco client <1-4> dm-result     # 客户端DM结果
display cfp2-dco client <1-4> loopmode      # 客户端环回模式
display cfp2-dco line dm-mode               # 线路侧DM模式
display cfp2-dco line dm-result             # 线路侧DM结果
display cfp2-dco line loopmode              # 线路侧环回模式
display cfp2-dco operation-mode             # 工作模式
display cfp2-dco freq-mini                  # 最小频率
display cfp2-dco cd-range                   # 色散范围

# 客户端口查询
display client <1-4> <tx-laser|als>         # 客户端激光器/ALS状态
display client <1-4> lf-debounce            # 链路故障去抖
display client <1-4> page <STRING> reg-addr <STRING>  # 寄存器读取

# 线路侧查询
display alarm-threshold line-rx-pow         # 线路接收功率告警阈值
display alarm-threshold pre-fec-high        # Pre-FEC误码率高告警阈值

# 其他查询
display operation-mode                      # 工作模式
display vega <general|real>                 # VEGA信息
display vega dielink_status                 # Die链路状态
display lldp <1-4>                          # LLDP信息
display statistic <1-4>                     # 统计信息
display fpga version                        # FPGA版本
```

### 9.3 配置命令

```bash
# 客户端口配置
config client <1-4> service <100ge|400ge>   # 配置客户端业务类型
config client <1-4> <tx-laser|als> <on|off> # 控制激光器/ALS
config client <1-4> lf <on|off>             # 链路故障设置
config client <1-4> lf-debounce <0-3000>    # 链路故障去抖时间
config client <1-4> lldp <enable|disable>   # LLDP设置
config client <1-4> duplex-als <on|off>     # 双工ALS

# 客户端口环回
config client <1-4> loopback <none|line|client|facility>  # 环回模式

# 客户端口复位
reset client <1-4>                          # 复位客户端口

# LLDP全局配置
config lldp global <enable|disable>         # 全局LLDP

# 线路侧配置
config line tx-power <STRING>               # 线路发送功率
config line rx-power <STRING>               # 线路接收功率
config line wavelength <STRING>             # 线路波长
config line frequency <STRING>              # 线路频率
config line modulation <QPSK|8QAM|16QAM>    # 调制格式
config line baud-rate <STRING>              # 波特率
config line fec <SD-FEC|HD-FEC>             # FEC类型
config line cd <STRING>                     # 色散补偿
```

---

## 十、典型配置流程

### 10.1 新设备上线配置

```bash
# 1. 登录设备（默认 admin/Admin_123）

# 2. 查看设备信息
<Accelink> display version
<Accelink> display ip-address

# 3. 进入全局配置视图
<Accelink> system-view
[Accelink]

# 4. 配置设备名称
[Accelink] sysname O2-Node-A

# 5. 配置IP地址
[Accelink] ip 1 address 10.1.1.1 255.255.255.0
[Accelink] gateway 1 add 10.1.1.254

# 6. 配置时区和时间
[Accelink] timezone name Asia/Shanghai
[Accelink] systime 2026/05/29/10/00/00

# 7. 配置NTP
[Accelink] ntp enable
[Accelink] ntp server add 10.1.1.100

# 8. 保存配置
[Accelink] save

# 9. 配置单盘
[Accelink] set slot 1/1 type olp
[Accelink] set slot 1/3 type oa
[Accelink] set slot 1/5 type wss
```

### 10.2 OLP保护配置

```bash
# 进入OLP视图
[Accelink] slot 1/1
[Accelink-OLP-1/1]

# 配置保护参数
[Accelink-OLP-1/1] relative-diff-threshold 5.0
[Accelink-OLP-1/1] switch hysteresis 1.0
[Accelink-OLP-1/1] hold-off-time 0
[Accelink-OLP-1/1] wait-to-restore-time 300

# 配置工作模式
[Accelink-OLP-1/1] workmode auto-reversion

# 配置告警阈值
[Accelink-OLP-1/1] common-in alarm threshold -13.0
[Accelink-OLP-1/1] primary-out alarm threshold -16.0
[Accelink-OLP-1/1] secondary-out alarm threshold -16.0
```

### 10.3 EDFA配置

```bash
# 进入EDFA视图
[Accelink] slot 1/3
[Accelink-OA-1/3]

# 配置EDFA
[Accelink-OA-1/3] edfa 1 enable
[Accelink-OA-1/3] edfa 1 gain 22.0
[Accelink-OA-1/3] edfa 1 tilt 0.0
[Accelink-OA-1/3] edfa 1 amp-mode agc

# 配置告警阈值
[Accelink-OA-1/3] edfa 1 input alarm-threshold -25.0
[Accelink-OA-1/3] edfa 1 output alarm-threshold 0.0
[Accelink-OA-1/3] edfa 1 input los threshold -28.0
```

### 10.4 WSS波长配置

```bash
# 进入WSS视图
[Accelink] slot 1/5
[Accelink-WSS-1/5]

# 添加波长通道（通道1，从端口1上波，目标功率-10dBm）
[Accelink-WSS-1/5] wss channel add 1 1 add -10.0 0.0

# 设置通道衰减
[Accelink-WSS-1/5] wss channel attenuation 1 add 3.0

# 启用通道
[Accelink-WSS-1/5] wss channel status 1 add enable
```

---

## 十一、常用维护命令速查

### 11.1 日常巡检

```bash
# 系统状态
display version
display systime
display cpu
display memory
display temperature
display fan
display power

# 告警检查
display alarm

# 网络检查
display ip-address
ping <网关IP>

# 单盘状态
display slot all
```

### 11.2 光功率检查

```bash
# OLP功率
display olp
display common-in
display primary-out
display secondary-out

# EDFA功率
display edfa
display edfa 1 pin
display edfa 1 pout

# WSS功率
display wss
display wss port 1 pin
display wss port 1 pout

# OCM光谱
display ocm 1 spectrum
```

### 11.3 故障排查

```bash
# 查看告警详情
display alarm

# 查看历史命令
display history

# 查看配置变更
display configuration modified

# OTDR测试（光纤断点）
display otdr 1 current-result
otdr 1 trigger

# 端口环回测试
config client 1 loopback line
config client 1 loopback none
```

---

## 十二、注意事项

1. **配置保存**：修改配置后务必执行 `save` 命令保存
2. **视图层级**：注意当前所在视图，不同视图命令不同
3. **参数范围**：注意命令参数的有效范围（如 `<1-8>`、`<STRING>`）
4. **告警阈值**：合理设置告警阈值，避免误告警
5. **保护倒换**：谨慎使用 `forcetoport` 强制倒换命令
6. **OTDR测试**：周期性OTDR测试会影响业务，注意设置合适周期

---

*老仙学习笔记 - 2026-05-29*
