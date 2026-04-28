#!/usr/bin/env python3
"""
港股实时行情图片生成器
"""
import urllib.request
import re
from PIL import Image, ImageDraw, ImageFont
import os

def get_hk_stock(codes):
    code_str = ','.join([f'hk{c}' for c in codes])
    url = f'https://qt.gtimg.cn/q={code_str}'
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read().decode('gbk', errors='ignore')
    
    result = {}
    for line in data.strip().split(';'):
        if not line.strip():
            continue
        match = re.search(r'v_(\w+)="([^"]+)"', line)
        if match:
            code, values = match.groups()
            fields = values.split('~')
            result[code] = {
                'name': fields[1] if len(fields) > 1 else '',
                'code': fields[2] if len(fields) > 2 else '',
                'price': fields[3] if len(fields) > 3 else '',
                'change': fields[31] if len(fields) > 31 else '',
                'change_percent': fields[32] if len(fields) > 32 else '',
                'high': fields[33] if len(fields) > 33 else '',
                'low': fields[34] if len(fields) > 34 else '',
            }
    return result

def create_stock_image(stocks, output_path):
    # 图片尺寸
    width = 800
    row_height = 80
    header_height = 100
    padding = 40
    
    height = header_height + len(stocks) * row_height + padding * 2
    
    # 创建图片
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        # macOS 系统字体
        font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
        font_medium = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    title = "🇭🇰 港股实时行情"
    draw.text((width//2, 30), title, fill='#ffffff', font=font_large, anchor='mt')
    
    # 绘制时间
    from datetime import datetime
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    draw.text((width//2, 70), time_str, fill='#888888', font=font_small, anchor='mt')
    
    # 绘制股票信息
    y = header_height + padding
    
    for code_key, stock in stocks.items():
        name = stock.get('name', '')
        code = stock.get('code', '')
        price = stock.get('price', '')
        change = stock.get('change', '')
        change_pct = stock.get('change_percent', '')
        high = stock.get('high', '')
        low = stock.get('low', '')
        
        # 判断涨跌颜色
        try:
            change_val = float(change) if change else 0
            if change_val > 0:
                color = '#00d26a'  # 涨 - 绿色（港股绿涨红跌）
                sign = '+'
            elif change_val < 0:
                color = '#ff4757'  # 跌 - 红色
                sign = ''
            else:
                color = '#aaaaaa'
                sign = ''
        except:
            color = '#aaaaaa'
            sign = ''
        
        # 绘制分隔线
        draw.line([(40, y), (width-40, y)], fill='#333333', width=1)
        
        # 股票名称和代码
        draw.text((60, y + 15), f"{name}", fill='#ffffff', font=font_medium)
        draw.text((60, y + 45), f"{code}", fill='#888888', font=font_small)
        
        # 价格
        draw.text((width//2, y + 30), f"{price}", fill=color, font=font_large, anchor='mm')
        
        # 涨跌幅
        change_text = f"{sign}{change} ({sign}{change_pct}%)"
        draw.text((width-60, y + 20), change_text, fill=color, font=font_medium, anchor='rt')
        
        # 最高最低
        hl_text = f"高:{high} 低:{low}"
        draw.text((width-60, y + 50), hl_text, fill='#888888', font=font_small, anchor='rt')
        
        y += row_height
    
    # 保存图片
    img.save(output_path, 'PNG')
    return output_path

if __name__ == '__main__':
    import sys
    codes = sys.argv[1:] if len(sys.argv) > 1 else ['HSI', '00700', '09988']
    
    print(f"正在获取 {', '.join(codes)} 的数据...")
    stocks = get_hk_stock(codes)
    
    output = os.path.expanduser('~/.openclaw/workspace/tools/hkstock/hkstock.png')
    create_stock_image(stocks, output)
    print(f"图片已保存: {output}")
