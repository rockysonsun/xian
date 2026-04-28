#!/usr/bin/env python3
"""
港股 K 线图生成器
使用 Pillow 绘制标准 K 线
"""
import urllib.request
import re
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import os

def get_hk_kline(code, days=30):
    """
    获取港股 K 线数据
    使用东方财富 API
    """
    # 转换代码格式
    if code == 'HSI':
        secid = '100.HSI'
    else:
        secid = f'116.{code}'
    
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d')
    
    url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=0&beg={start_date}&end={end_date}'
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        klines = []
        if data.get('data') and data['data'].get('klines'):
            for line in data['data']['klines'][-days:]:
                # 格式: 日期,开盘,收盘,最低,最高,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
                parts = line.split(',')
                klines.append({
                    'date': parts[0],
                    'open': float(parts[1]),
                    'close': float(parts[2]),
                    'low': float(parts[4]),
                    'high': float(parts[3]),
                    'volume': float(parts[5]),
                })
        return klines
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

def draw_kline_chart(klines, title, output_path, width=1200, height=800):
    """绘制 K 线图 """
    if not klines:
        print("没有数据可绘制")
        return
    
    # 创建图片
    img = Image.new('RGB', (width, height), color='#0d1117')
    draw = ImageDraw.Draw(img)
    
    # 边距
    margin_left = 80
    margin_right = 100
    margin_top = 60
    margin_bottom = 100
    
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    
    # 计算价格范围
    all_highs = [k['high'] for k in klines]
    all_lows = [k['low'] for k in klines]
    max_price = max(all_highs)
    min_price = min(all_lows)
    price_range = max_price - min_price
    padding = price_range * 0.1
    max_price += padding
    min_price -= padding
    price_range = max_price - min_price
    
    # 字体 - 尝试多个中文字体
    font_title = font_label = font_small = ImageFont.load_default()
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for font_path in font_paths:
        try:
            font_title = ImageFont.truetype(font_path, 28)
            font_label = ImageFont.truetype(font_path, 14)
            font_small = ImageFont.truetype(font_path, 12)
            break
        except:
            continue
    
    # 绘制标题
    draw.text((width//2, 30), f"📈 {title} K线图", fill='#ffffff', font=font_title, anchor='mt')
    
    # 绘制网格线
    grid_color = '#21262d'
    for i in range(6):
        y = margin_top + (chart_height * i // 5)
        draw.line([(margin_left, y), (margin_left + chart_width, y)], fill=grid_color, width=1)
    
    # 绘制价格标签
    for i in range(6):
        price = max_price - (price_range * i // 5)
        y = margin_top + (chart_height * i // 5)
        draw.text((margin_left - 10, y), f"{price:.2f}", fill='#8b949e', font=font_small, anchor='rm')
    
    # 绘制 K 线
    n = len(klines)
    candle_width = chart_width // (n * 2)
    if candle_width < 2:
        candle_width = 2
    spacing = chart_width // n
    
    for i, k in enumerate(klines):
        x = margin_left + (i * spacing) + (spacing // 2)
        
        # 计算 Y 坐标
        y_open = margin_top + chart_height - ((k['open'] - min_price) / price_range * chart_height)
        y_close = margin_top + chart_height - ((k['close'] - min_price) / price_range * chart_height)
        y_high = margin_top + chart_height - ((k['high'] - min_price) / price_range * chart_height)
        y_low = margin_top + chart_height - ((k['low'] - min_price) / price_range * chart_height)
        
        # 确定颜色（港股：绿涨红跌）
        if k['close'] > k['open']:
            color = '#00d26a'  # 涨 - 绿色
        elif k['close'] < k['open']:
            color = '#ff4757'  # 跌 - 红色
        else:
            color = '#8b949e'  # 平 - 灰色
        
        # 绘制影线
        draw.line([(x, y_high), (x, y_low)], fill=color, width=1)
        
        # 绘制实体
        body_top = min(y_open, y_close)
        body_bottom = max(y_open, y_close)
        body_height = max(1, body_bottom - body_top)
        
        draw.rectangle(
            [(x - candle_width//2, body_top), (x + candle_width//2, body_bottom)],
            fill=color,
            outline=color
        )
    
    # 绘制边框
    draw.rectangle(
        [(margin_left, margin_top), (margin_left + chart_width, margin_top + chart_height)],
        outline='#30363d',
        width=1
    )
    
    # 绘制日期标签（只显示部分）
    label_step = max(1, n // 6)
    for i in range(0, n, label_step):
        k = klines[i]
        x = margin_left + (i * spacing) + (spacing // 2)
        date_str = k['date'][5:]  # 取 MM-DD
        draw.text((x, margin_top + chart_height + 10), date_str, fill='#8b949e', font=font_small, anchor='mt')
    
    # 保存
    img.save(output_path, 'PNG')
    print(f"K线图已保存: {output_path}")
    return output_path

if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else 'HSI'
    name_map = {
        'HSI': '恒生指数',
        '00700': '腾讯控股',
        '09988': '阿里巴巴',
        '03690': '美团',
        '01810': '小米集团',
    }
    name = name_map.get(code, code)
    
    print(f"正在获取 {name} ({code}) 的 K 线数据...")
    klines = get_hk_kline(code, days=30)
    
    if klines:
        output = os.path.expanduser(f'~/.openclaw/workspace/tools/hkstock/kline_{code}.png')
        draw_kline_chart(klines, name, output)
    else:
        print("获取数据失败，请检查代码是否正确")
