# 港股行情技能文档

## 技能列表

### 1. 实时行情查询
**文件**: `hkstock_query.py`
**用法**:
```bash
python3 ~/.openclaw/workspace/tools/hkstock/hkstock_query.py [代码1] [代码2] ...
```
**示例**:
```bash
python3 ~/.openclaw/workspace/tools/hkstock/hkstock_query.py HSI 00700 09988
```
**数据源**: 腾讯财经接口 `https://qt.gtimg.cn/`

---

### 2. K 线图生成（图片）
**文件**: `kline_chart.py`
**用法**:
```bash
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py [代码]
```
**示例**:
```bash
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py HSI      # 恒生指数
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py 00700    # 腾讯
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py 09988    # 阿里
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py 09626    # B站
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py 03690    # 美团
python3 ~/.openclaw/workspace/tools/hkstock/kline_chart.py 01810    # 小米
```
**输出**: `~/.openclaw/workspace/tools/hkstock/kline_[代码].png`
**数据源**: 东方财富接口 `https://push2his.eastmoney.com/`
**依赖**: Pillow (Python 图像库)

---

### 3. 实时行情网页
**文件**: `hkstock_html.py`
**用法**:
```bash
python3 ~/.openclaw/workspace/tools/hkstock/hkstock_html.py [代码1] [代码2] ...
```
**输出**: `~/.openclaw/workspace/tools/hkstock/hkstock.html`

---

### 4. K 线图网页（交互式）
**文件**: `kline_web.py`
**用法**:
```bash
python3 ~/.openclaw/workspace/tools/hkstock/kline_web.py [代码]
```
**输出**: `~/.openclaw/workspace/tools/hkstock/kline_chart.html`
**特点**: 使用 TradingView Lightweight Charts，支持鼠标交互

---

## 常用港股代码

| 代码 | 名称 |
|------|------|
| HSI | 恒生指数 |
| 00700 | 腾讯控股 |
| 09988 | 阿里巴巴-W |
| 09626 | 哔哩哔哩-W |
| 03690 | 美团-W |
| 01810 | 小米集团-W |
| 02015 | 理想汽车-W |
| 09888 | 百度集团-SW |
| 01024 | 快手-W |
| 06060 | 众安在线 |

---

## 技术细节

### 数据源
1. **实时数据**: 腾讯财经 `qt.gtimg.cn` - 返回 GBK 编码文本
2. **历史 K 线**: 东方财富 `push2his.eastmoney.com` - 返回 JSON

### 港股配色规则
- 🟢 绿色 = 上涨（港股惯例）
- 🔴 红色 = 下跌
- ⚪ 灰色 = 平盘

### 依赖安装
```bash
# 图片生成需要 Pillow
pip3 install Pillow

# 网页版需要网络连接加载 TradingView JS 库
```

---

## 更新记录

- 2026-03-09: 初始版本，支持实时查询、K线图生成、网页展示

---

**注意**: 本技能由星宿老仙（M78 星云数码生命体）开发维护 🌟
