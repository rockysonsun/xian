#!/usr/bin/env python3
"""
港股实时行情 HTML 生成器
生成美观的 HTML 页面，可在浏览器中打开或截图
"""
import urllib.request
import re
import os
from datetime import datetime

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

def create_stock_html(stocks, output_path):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>港股实时行情</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 40px;
            color: #fff;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header .time {{
            color: #888;
            font-size: 14px;
        }}
        .stock-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .stock-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .stock-name {{
            font-size: 20px;
            font-weight: 600;
        }}
        .stock-code {{
            color: #888;
            font-size: 14px;
            margin-left: 8px;
        }}
        .stock-price {{
            font-size: 28px;
            font-weight: 700;
        }}
        .stock-change {{
            font-size: 16px;
            margin-top: 4px;
        }}
        .stock-hl {{
            color: #888;
            font-size: 13px;
            margin-top: 8px;
        }}
        .up {{ color: #00d26a; }}
        .down {{ color: #ff4757; }}
        .flat {{ color: #aaaaaa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇭🇰 港股实时行情</h1>
            <div class="time">{time_str}</div>
        </div>
'''
    
    for code_key, stock in stocks.items():
        name = stock.get('name', '')
        code = stock.get('code', '')
        price = stock.get('price', '')
        change = stock.get('change', '')
        change_pct = stock.get('change_percent', '')
        high = stock.get('high', '')
        low = stock.get('low', '')
        
        try:
            change_val = float(change) if change else 0
            if change_val > 0:
                color_class = 'up'
                sign = '+'
            elif change_val < 0:
                color_class = 'down'
                sign = ''
            else:
                color_class = 'flat'
                sign = ''
        except:
            color_class = 'flat'
            sign = ''
        
        html += f'''
        <div class="stock-card">
            <div class="stock-header">
                <div>
                    <span class="stock-name">{name}</span>
                    <span class="stock-code">{code}</span>
                </div>
                <div style="text-align: right;">
                    <div class="stock-price {color_class}">{price}</div>
                    <div class="stock-change {color_class}">{sign}{change} ({sign}{change_pct}%)</div>
                </div>
            </div>
            <div class="stock-hl">最高: {high} &nbsp;|&nbsp; 最低: {low}</div>
        </div>
'''
    
    html += '''
    </div>
</body>
</html>
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path

if __name__ == '__main__':
    import sys
    codes = sys.argv[1:] if len(sys.argv) > 1 else ['HSI', '00700', '09988']
    
    print(f"正在获取 {', '.join(codes)} 的数据...")
    stocks = get_hk_stock(codes)
    
    output = os.path.expanduser('~/.openclaw/workspace/tools/hkstock/hkstock.html')
    create_stock_html(stocks, output)
    print(f"HTML 已生成: {output}")
    print(f"请在浏览器中打开查看，或用浏览器截图功能保存为图片")
