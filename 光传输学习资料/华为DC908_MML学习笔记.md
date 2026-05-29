# 华为 DC908 MML 命令行学习笔记

> 学习来源：OptiXtrans DC908 V100R021C10SPC300命令行手册 (76268段)
> 学习时间：2026-05-29

---

## 一、MML 概述

### 1.1 MML 定义

**MML（Man Machine Language）** 是通过字符串的方式，将命令以及相关的参数传递给网元执行，执行的结果同样以字符形式呈现给用户的操作和维护接口。

- 相对于图形界面，操作效率更高，适合高级用户使用
- 界面友好性较差，但功能更强大

### 1.2 MML 工具

| 工具类型 | 协议 | 端口 | 访问范围 |
|----------|------|------|----------|
| SSH终端（如Putty） | SSHv2 | 22 | 仅网关网元（近端） |
| 网管CmdClient | TLS 1.1/1.2/1.3 | 5432 | 网关+非网关网元（远程） |

### 1.3 MML 输入输出格式

**命令下发格式：**
```
命令行提示> 命令字符串 [空格] [参数1], [参数2], … [参数n]
```

**设置/操作类命令返回：**
```
命令行提示>
命令执行结果（成功或失败）
```

**查询类命令返回：**
```
命令行提示>
Table Head
Table1		[Table2]	[Table3]	[…]		[Tablen]
Result		[Result]		[Result]		[…]
Total record: m
命令行提示>
```

---

## 二、命令分类体系

### 2.1 命令前缀分类

华为 DC908 共有 **6359+ 个命令**，按前缀分类：

| 前缀 | 数量 | 功能领域 |
|------|------|----------|
| `cfg-` | 2237 | 配置管理（核心命令） |
| `cm-` | 823 | 通信管理（DCN、隧道等） |
| `lim-` | 382 | 线路接口模块调试 |
| `sm-` | 274 | 系统管理 |
| `per-` | 184 | 性能管理 |
| `mon-` | 165 | 监控模块 |
| `alm-` | 136 | 告警管理 |
| `swdl-` | 122 | 软件加载 |
| `emca-` | 96 | 光层自动调测 |
| `dbms-` | 94 | 数据库管理 |
| `ops-` | 92 | 光保护倒换 |
| `sftm-` | 92 | 软件管理 |
| `pm-` | 88 | 性能监测 |
| `libm-` | 80 | 交叉连接模块 |
| `secu-` | 78 | 安全管理 |
| `snmp-` | 66 | SNMP协议 |

### 2.2 cfg- 命令子分类

| 子分类 | 数量 | 说明 |
|--------|------|------|
| `cfg-get-*` | 1212 | 查询类命令 |
| `cfg-set-*` | 793 | 设置类命令 |
| `cfg-add-*` | 48 | 添加类命令 |
| `cfg-del-*` | 54 | 删除类命令 |
| `cfg-check-*` | 4 | 检查类命令 |
| `cfg-other` | 126 | 其他操作 |

---

## 三、主要功能模块

### 3.1 网元管理（第2章）

**核心命令：**

```bash
# 设备信息查询
cfg-get-devicetype              # 查询设备类型
cfg-get-nename                  # 查询网元名称
cfg-set-nename:<name>           # 设置网元名称
cfg-get-version                 # 查询版本信息
cfg-get-shelf                   # 查询机框信息
cfg-get-physhelf                # 查询物理机框

# 系统配置
cfg-get-nepsmode                # 查询电源模式
cfg-set-nepsmode:<mode>         # 设置电源模式
cfg-get-xccapacity              # 查询交叉容量
cfg-get-shelf-tempth            # 查询机框温度阈值
cfg-set-sdexc-almth             # 设置SD告警阈值

# 许可和授权
cfg-get-licenseinfo             # 查询许可证信息
cfg-set-licenseinfo             # 设置许可证
cfg-get-ne-license              # 查询网元许可

# 其他
cfg-get-operator-info           # 查询操作员信息
cfg-set-operator-info           # 设置操作员信息
cfg-get-nememo                  # 查询网元备注
cfg-set-nememo:<memo>           # 设置网元备注
cfg-get-neposition              # 查询网元位置
cfg-set-neposition:<pos>        # 设置网元位置
```

### 3.2 单板管理（第3章）

**通用单板管理：**

```bash
# 单板信息查询
cfg-get-board:<bid>             # 查询单板信息
cfg-get-phybd:<bid>             # 查询物理单板
cfg-get-bdversion:<bid>         # 查询单板版本
cfg-get-bdverinfo:<bid>         # 查询版本详细信息
cfg-get-workstat:<bid>          # 查询工作状态
cfg-get-ledstate:<bid>          # 查询LED状态
cfg-set-ledstate:<bid>,<state>  # 设置LED状态

# 温度管理
cfg-get-bdtempth:<bid>          # 查询单板温度阈值
cfg-set-bdtempth:<bid>,<th>     # 设置温度阈值
cfg-get-tempover-almen:<bid>    # 查询温度越限使能
cfg-set-tempover-almen:<bid>,<en> # 设置温度越限使能
cfg-get-tempover-almth:<bid>    # 查询温度越限阈值
cfg-set-tempover-almth:<bid>,<th> # 设置温度越限阈值

# 单板操作
cfg-replace-board:<bid>,<type>  # 替换单板
cfg-modify-board:<bid>,<param>  # 修改单板
cfg-set-subbdtype:<bid>,<type>  # 设置子卡类型
cfg-get-subbdtype:<bid>         # 查询子卡类型

# 端口光放直通
cfg-get-portoampass:<bid>,<port> # 查询光放直通
cfg-set-portoampass:<bid>,<port>,<en> # 设置光放直通
```

**EFI单板管理：**

```bash
cfg-set-relayswitch:<bid>,<switch>,<state>   # 设置继电器开关
cfg-get-relayswitch:<bid>                    # 查询继电器开关
cfg-set-switchalmlevel:<bid>,<level>         # 设置开关告警级别
cfg-get-switchalmlevel:<bid>                 # 查询开关告警级别
```

### 3.3 光模块管理（第4章）

**激光器控制：**

```bash
# 激光器开关
cfg-set-laser:<bid>,<port>,<path>,<state>    # 设置激光器开关
cfg-get-laser:<bid>,<port>,<path>            # 查询激光器状态

# ALS（自动激光器关断）
cfg-set-als:<bid>,<port>,<path>,<state>      # 设置ALS
cfg-get-als:<bid>,<port>,<path>              # 查询ALS状态
cfg-set-alsdelay:<bid>,<port>,<path>,<delay> # 设置ALS延迟
cfg-get-alsdelay:<bid>,<port>,<path>         # 查询ALS延迟
cfg-set-alsopendelay:<bid>,<port>,<path>,<delay> # 设置ALS打开延迟
cfg-get-alsopendelay:<bid>,<port>,<path>     # 查询ALS打开延迟
cfg-set-alscond:<bid>,<port>,<path>,<cond>   # 设置ALS条件
cfg-get-alscond:<bid>,<port>,<path>          # 查询ALS条件
```

**光功率查询：**

```bash
# 输入/输出光功率
cfg-get-inpower:<bid>,<port>,<path>          # 查询输入光功率
cfg-get-outpower:<bid>,<port>,<path>         # 查询输出光功率

# 输出格式示例：
# "INPOWER"
# "BID" "PORT" "PATH" "INPOWER"
# <槽位号> <光口号> <通道号> <输入光功率>
```

**波长配置：**

```bash
# 波长设置
cfg-set-wavelen:<bid>,<port>,<path>,<wavelen>   # 设置波长
cfg-get-wavelen:<bid>,<port>,<path>             # 查询当前波长
cfg-get-cfgwavelen:<bid>,<port>,<path>          # 查询配置波长
cfg-get-waverange:<bid>,<port>,<path>           # 查询波长范围

# 细波配置（Gridless）
cfg-set-slicewavelen:<bid>,<port>,<path>,<freq> # 设置细波中心频率
cfg-get-slicewavelen:<bid>,<port>,<path>        # 查询细波中心频率
cfg-get-cfg-slicewavelen:<bid>,<port>,<path>    # 查询配置细波
cfg-get-slicewave-range:<bid>,<port>,<path>     # 查询细波范围
cfg-set-recslicewavelen:<bid>,<port>,<path>,<freq> # 设置接收细波
cfg-get-recslicewavelen:<bid>,<port>,<path>     # 查询接收细波
```

**发送功率配置：**

```bash
cfg-get-cfgoutpower:<bid>,<port>,<path>        # 查询配置输出光功率
cfg-set-outpower:<bid>,<port>,<path>,<power>   # 设置输出光功率
cfg-get-outpower-range:<bid>,<port>,<path>     # 查询输出功率范围

# 输出格式：
# "OTUPOWER RANGE"
# "BID", "PORT", "PATH", "ENABLE", "TH-HIGH", "TH-LOW"
```

**告警阈值：**

```bash
cfg-set-almth:<bid>,<port>,<path>,<type>,<th>  # 设置告警阈值
cfg-get-almth:<bid>,<port>,<path>,<type>        # 查询告警阈值
cfg-get-default-almth:<bid>,<port>,<path>       # 查询默认告警阈值
cfg-get-almth-range:<bid>,<port>,<path>,<type>  # 查询告警阈值范围
```

**其他光模块命令：**

```bash
cfg-get-modetype:<bid>,<port>,<path>           # 查询模块类型
cfg-get-pmdth:<bid>,<port>,<path>              # 查询PMD阈值
cfg-get-lpt:<bid>,<port>,<path>                # 查询LPT（链路保护）
cfg-set-lpt:<bid>,<port>,<path>,<state>        # 设置LPT
cfg-get-modverinfo:<bid>                       # 查询光模块微程序版本
cfg-get-omodinfo:<bid>,<port>                  # 查询光模块信息
cfg-set-omodcfgflag:<bid>,<port>,<flag>        # 设置光模块配置标志
cfg-get-omodcfgflag:<bid>,<port>               # 查询光模块配置标志
cfg-monitor-omodinfo:<bid>,<port>,<state>      # 监控光模块信息
cfg-set-omodmonstate:<bid>,<port>,<state>      # 设置光模块监控状态
```

### 3.4 环回测试（第5章）

```bash
cfg-set-loop:<bid>,<port>,<path>,<type>        # 设置环回
# type: none(无环回), line(线路环回), client(客户端环回), facility(设备环回)
```

### 3.5 OTN 管理（第6章）

```bash
# OTN告警阈值
cfg-get-default-almth-ex:<bid>,<port>,<path>   # 查询扩展默认告警阈值

# OTU/ODU配置
cfg-set-payloadtype:<bid>,<port>,<path>,<type>  # 设置净荷类型
cfg-get-payloadtype:<bid>,<port>,<path>         # 查询净荷类型

# FEC配置
cfg-set-fecmode:<bid>,<port>,<path>,<mode>      # 设置FEC模式
cfg-get-fecmode:<bid>,<port>,<path>             # 查询FEC模式

# 时隙配置
cfg-set-oduts:<bid>,<port>,<path>,<ts>          # 设置ODU时隙
cfg-get-oduts:<bid>,<port>,<path>               # 查询ODU时隙
```

### 3.6 业务配置（第7章）

```bash
# 交叉连接
cfg-add-xc:<src>,<dst>,<type>                   # 添加交叉连接
cfg-del-xc:<xcid>                               # 删除交叉连接
cfg-get-xc:<type>                               # 查询交叉连接

# 业务配置
cfg-set-sdhbus:<bid>,<bus>,<state>              # 设置SDH总线
cfg-get-sdhbus:<bid>,<bus>                      # 查询SDH总线
```

### 3.7 以太网配置（第8章）

```bash
# MTU配置
cfg-set-mtu:<bid>,<port>,<mtu>                  # 设置MTU
cfg-get-mtu:<bid>,<port>                        # 查询MTU

# 端口属性
cfg-set-portattr:<bid>,<port>,<attr>,<val>      # 设置端口属性
cfg-get-portattr:<bid>,<port>,<attr>            # 查询端口属性

# VLAN配置
cfg-add-vlan:<vlanid>                           # 添加VLAN
cfg-del-vlan:<vlanid>                           # 删除VLAN
cfg-get-vlan:<vlanid>                           # 查询VLAN

# MAC地址
cfg-get-macaddr:<bid>,<port>                    # 查询MAC地址
cfg-get-maccount:<bid>,<port>                   # 查询MAC数量
```

### 3.8 端口管理（第9章）

```bash
# 端口信息
cfg-get-port:<bid>,<port>                       # 查询端口信息
cfg-get-allport:<bid>                           # 查询所有端口
cfg-get-phyport:<bid>,<port>                    # 查询物理端口

# 端口状态
cfg-set-portstate:<bid>,<port>,<state>          # 设置端口状态
cfg-get-portstate:<bid>,<port>                  # 查询端口状态

# 监控端口
cfg-set-mon-port:<bid>,<port>,<monbid>,<monport> # 设置监控端口
cfg-get-mon-port:<bid>,<port>                   # 查询监控端口
```

### 3.9 色散补偿（第10章）

```bash
cfg-get-dcm:<bid>                               # 查询DCM信息
cfg-set-dcm:<bid>,<type>,<value>                # 设置DCM
cfg-add-dcm-info:<bid>,<type>,<param>           # 添加DCM信息
cfg-del-dcm-info:<bid>                          # 删除DCM信息
```

### 3.10 PRBS测试（第11章）

```bash
cfg-set-prbs:<bid>,<port>,<path>,<type>         # 设置PRBS
cfg-get-prbs:<bid>,<port>,<path>                # 查询PRBS
cfg-clr-prbsresult:<bid>,<port>,<path>          # 清除PRBS结果
cfg-get-prbsresult:<bid>,<port>,<path>          # 查询PRBS结果
```

### 3.11 RFC2544测试（第12章）

```bash
cfg-start-rfc2544:<bid>,<port>,<param>          # 启动RFC2544测试
cfg-stop-rfc2544:<bid>,<port>                   # 停止RFC2544测试
cfg-get-rfc2544result:<bid>,<port>              # 查询测试结果
```

### 3.12 交叉板M:N保护（第13章）

```bash
cfg-get-dps:<dpsid>                             # 查询保护组
cfg-set-dps:<dpsid>,<param>                     # 设置保护组
cfg-set-dpsswitch:<dpsid>,<cmd>                 # 保护倒换命令
# cmd: lock(锁定), force(强制倒换), manual(人工倒换), clear(清除)
```

### 3.13 系统管理（第14章）

```bash
# 系统重启
cfg-reboot:<type>                               # 系统重启
# type: warm(热重启), cold(冷重启)

# 数据库操作
cfg-backup-db:<type>                            # 备份数据库
cfg-restore-db:<filename>                       # 恢复数据库

# 配置文件
cfg-export-config:<filename>                    # 导出配置
cfg-import-config:<filename>                    # 导入配置

# 时间同步
cfg-set-systime:<time>                          # 设置系统时间
cfg-get-systime                                 # 查询系统时间
cfg-set-timezone:<zone>                         # 设置时区
cfg-get-timezone                                # 查询时区
```

### 3.14 风扇管理（第15章）

```bash
cfg-get-fan:<fanid>                             # 查询风扇信息
cfg-set-fanspeed:<fanid>,<speed>                # 设置风扇转速
cfg-get-fan-avgspeed:<fanid>                    # 查询风扇平均转速
```

### 3.15 电源管理（第16章）

```bash
cfg-get-piu:<piuid>                             # 查询电源接口单元
cfg-get-piu-realvolt:<piuid>                    # 查询电源实际电压
cfg-set-piu-th:<piuid>,<th>                     # 设置电源阈值
```

### 3.16 光纤管理（第17章）

**光纤管理：**

```bash
# 光纤管理配置
cfg-add-fibermgr:<bid>,<port>,<param>           # 添加光纤管理
cfg-del-fibermgr:<bid>,<port>                   # 删除光纤管理
cfg-get-fibermgr:<bid>,<port>                   # 查询光纤管理
cfg-get-fibermgr-ex:<bid>,<port>                # 扩展查询光纤管理
cfg-add-fibermgr-ex:<bid>,<port>,<param>        # 扩展添加光纤管理
cfg-del-fibermgr-ex:<bid>,<port>                # 扩展删除光纤管理
```

**OTDR测试：**

```bash
# 一键OTDR测试
cfg-onekey-start-otdr:<bid>,<port>,<path>,<mode>,<pulse>,<time>,<range>
# mode: ManualOnline(手动在线), AutoOnline(自动在线)
# pulse: 脉冲宽度(10-20000ns)
# time: 平均时间(10-180s)
# range: 距离范围(5-260km)

# OTDR事件阈值
cfg-get-otdr-event-threshold:<bid>,<port>,<path>    # 查询OTDR事件阈值
cfg-set-otdr-event-threshold:<bid>,<port>,<path>,<reflection>,<spliceloss>,<endfiber>
# reflection: 反射事件阈值(0.01dB)
# spliceloss: 熔接损耗阈值(0.01dB)
# endfiber: 光纤末端阈值(m)

# OTDR周期检测
cfg-get-otdr-period-detect:<bid>,<port>             # 查询周期检测参数
cfg-set-otdr-period-detect:<bid>,<port>,<en>,<period> # 设置周期检测

# OTDR文件管理
cfg-get-otdr-sor-save-mode:<bid>                    # 查询SOR保存模式
cfg-set-otdr-sor-save-mode:<bid>,<mode>             # 设置SOR保存模式
cfg-get-otdr-sor-index:<bid>,<port>,<index>         # 查询SOR索引
cfg-update-otdr-baseline-file:<bid>,<port>,<file>   # 更新基线文件
cfg-del-otdr-sor-file:<bid>,<port>,<file>           # 删除SOR文件

# OTDR告警参数
cfg-get-otdr-alm-para:<bid>,<port>                  # 查询OTDR告警参数
cfg-set-otdr-alm-para:<bid>,<port>,<param>          # 设置OTDR告警参数
```

### 3.17 端口保护（第18章）

```bash
# OLP保护
cfg-get-olp:<olpid>                                 # 查询OLP保护组
cfg-set-olp:<olpid>,<param>                         # 设置OLP保护组
cfg-olp-switch:<olpid>,<cmd>                        # OLP倒换命令

# 光通道保护
cfg-get-ochprot:<protid>                            # 查询光通道保护
cfg-set-ochprot:<protid>,<param>                    # 设置光通道保护

# 客户侧保护
cfg-get-clientprot:<protid>                         # 查询客户侧保护
cfg-set-clientprot:<protid>,<param>                 # 设置客户侧保护
```

### 3.18 维护命令（第19章）

```bash
# 性能查询
cfg-get-pm:<bid>,<port>,<path>,<granularity>        # 查询性能监测
# granularity: 15min, 24h

# 告警查询
cfg-get-alarm:<bid>,<type>                          # 查询告警
# type: current(当前), history(历史)

# 事件查询
cfg-get-event:<type>                                # 查询事件

# 日志查询
cfg-get-log:<type>,<starttime>,<endtime>            # 查询日志
```

### 3.19 通信管理（第20章）

```bash
# DCN配置
cfg-get-dcn                                         # 查询DCN配置
cfg-set-dcn:<param>                                 # 设置DCN配置

# 隧道管理（GRE）
cm-add-gre-tunnel:<param>                           # 添加GRE隧道
cm-set-gre-tunnel:<tunnelid>,<param>                # 设置GRE隧道
cm-del-gre-tunnel:<tunnelid>                        # 删除GRE隧道
cm-get-gre-tunnel:<tunnelid>                        # 查询GRE隧道
cm-test-tunnel:<tunnelid>                           # 测试隧道
cm-test-tunnel-result:<tunnelid>                    # 查询测试结果
```

### 3.20 同步时钟（第21章）

```bash
# 时钟源配置
cfg-get-clocksrc:<srcid>                            # 查询时钟源
cfg-set-clocksrc:<srcid>,<param>                    # 设置时钟源

# 时钟状态
cfg-get-clockstatus                                 # 查询时钟状态

# SSM配置
cfg-get-ssm:<bid>,<port>                            # 查询SSM
cfg-set-ssm:<bid>,<port>,<ssm>                      # 设置SSM

# PTP配置
cfg-get-ptp:<bid>,<port>                            # 查询PTP
cfg-set-ptp:<bid>,<port>,<param>                    # 设置PTP
```

### 3.21 WSS配置（第52章综合特性）

```bash
# WSS通道配置
cfg-add-wss-channel:<bid>,<port>,<channel>,<param>  # 添加WSS通道
cfg-add-wss-channel-ext:<bid>,<port>,<channel>,<param> # 扩展添加
cfg-del-wss-channel:<bid>,<port>,<channel>           # 删除WSS通道
cfg-del-wss-channel-ext:<bid>,<port>,<channel>       # 扩展删除
cfg-get-wss-channel:<bid>,<port>,<channel>           # 查询WSS通道

# WSS环回
cfg-add-wssloop:<bid>,<port>,<loopparam>             # 添加WSS环回
cfg-del-wssloop:<bid>,<port>                         # 删除WSS环回
cfg-get-wssloop:<bid>,<port>                         # 查询WSS环回

# WSS OPM端口
cfg-del-wss-opmport:<bid>,<port>                     # 删除WSS OPM端口

# WSS自动发现
afd-start-wss-discovery:<bid>                        # 启动WSS自动发现
```

---

## 四、常用命令速查表

### 4.1 日常巡检命令

```bash
# 系统状态
cfg-get-devicetype
cfg-get-nename
cfg-get-version
cfg-get-shelf
cfg-get-shelf-tempth

# 单板状态
cfg-get-board:1
cfg-get-workstat:1
cfg-get-bdversion:1

# 光功率检查
cfg-get-inpower:1,1,1
cfg-get-outpower:1,1,1

# 告警检查
cfg-get-alarm:1,current

# 性能检查
cfg-get-pm:1,1,1,15min
```

### 4.2 业务配置流程

```bash
# 1. 查询单板状态
cfg-get-board:<bid>

# 2. 配置波长
cfg-set-wavelen:<bid>,<port>,<path>,<wavelen>

# 3. 设置光功率
cfg-set-outpower:<bid>,<port>,<path>,<power>

# 4. 打开激光器
cfg-set-laser:<bid>,<port>,<path>,on

# 5. 配置交叉连接
cfg-add-xc:<src>,<dst>,<type>

# 6. 检查业务状态
cfg-get-port:<bid>,<port>
cfg-get-inpower:<bid>,<port>,<path>
cfg-get-outpower:<bid>,<port>,<path>
```

### 4.3 故障排查命令

```bash
# 告警查询
cfg-get-alarm:1,current
cfg-get-alarm:1,history

# 光功率检查
cfg-get-inpower:<bid>,<port>,<path>
cfg-get-outpower:<bid>,<port>,<path>

# 激光器状态
cfg-get-laser:<bid>,<port>,<path>

# 环回测试
cfg-set-loop:<bid>,<port>,<path>,line    # 线路环回
cfg-set-loop:<bid>,<port>,<path>,client  # 客户端环回
cfg-set-loop:<bid>,<port>,<path>,none    # 清除环回

# PRBS测试
cfg-set-prbs:<bid>,<port>,<path>,<type>
cfg-get-prbsresult:<bid>,<port>,<path>

# OTDR测试
cfg-onekey-start-otdr:<bid>,<port>,<path>,ManualOnline,20000,120,120

# 保护倒换状态
cfg-get-olp:<olpid>
cfg-get-dps:<dpsid>
```

---

## 五、与光迅 O2 对比

| 特性 | 华为 DC908 | 光迅 O2 |
|------|-----------|---------|
| **命令风格** | MML格式 `:cmd:param1,param2;` | 类Cisco IOS风格 `cmd param` |
| **视图层级** | 扁平结构，命令前缀区分 | 分层视图（预览→全局→单盘） |
| **命令数量** | 6359+ 个 | 约200+ 个 |
| **光模块管理** | `cfg-get-inpower/outpower` | `display edfa pin/pout` |
| **波长配置** | `cfg-set-wavelen` | `wss channel add` |
| **OTDR** | `cfg-onekey-start-otdr` | `otdr trigger` |
| **保护配置** | `cfg-set-olp` + `cfg-set-dps` | OLP单盘视图命令 |
| **WSS配置** | `cfg-add-wss-channel` | `wss channel add` |
| **登录方式** | SSH(22) / TLS(5432) | Telnet/SSH |
| **默认用户** | 需配置 | admin/Admin_123 |

---

## 六、注意事项

1. **命令格式**：华为 MML 命令使用冒号分隔，参数用逗号分隔，以分号结尾
2. **参数类型**：注意区分位置定义参数和关键字参数
3. **重复方式**：部分命令支持参数重复（如批量查询多个槽位）
4. **命令级别**：分为系统监视、系统操作等级别，注意权限
5. **开放范围**：用户级、管理员级等，影响可执行命令
6. **版本兼容性**：部分命令有版本要求（如 V5.99.52.00+）

---

*老仙学习笔记 - 2026-05-29*
