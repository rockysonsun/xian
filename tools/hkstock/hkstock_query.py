#!/usr/bin/env python3
"""
港股实时行情查询工具
用法: python3 hkstock_query.py [股票代码1] [股票代码2] ...
示例: python3 hkstock_query.py HSI 00700 09988
"""
import urllib.request
import re
import sys

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

def format_stock(stock):
    name = stock.get('name', '')
    code = stock.get('code', '')
    price = stock.get('price', '')
    change = stock.get('change', '')
    change_pct = stock.get('change_percent', '')
    high = stock.get('high', '')
    low = stock.get('low', '')
    
    try:
        change_val = float(change) if change else 0
        emoji = '📈' if change_val >= 0 else '📉'
        sign = '+' if change_val >= 0 else ''
    except:
        emoji = '➖'
        sign = ''
    
    return f"{emoji} {name} ({code}) | {price} | {sign}{change} ({sign}{change_pct}%) | 高:{high} 低:{low}"

if __name__ == '__main__':
    codes = sys.argv[1:] if len(sys.argv) > 1 else ['HSI', '00700', '09988']
    stocks = get_hk_stock(codes)
    
    for code in codes:
        key = f'hk{code}'
        if key in stocks:
            print(format_stock(stocks[key]))
