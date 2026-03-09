#!/usr/bin/env python3
"""
港股实时行情抓取
使用腾讯财经接口 (纯标准库)
"""
import urllib.request
import urllib.parse
import re

def get_hk_stock(codes):
    """
    获取港股实时行情
    codes: 股票代码列表，如 ['HSI', '00700', '09988']
    """
    # 构建请求
    code_str = ','.join([f'hk{c}' for c in codes])
    url = f'https://qt.gtimg.cn/q={code_str}'
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    with urllib.request.urlopen(req, timeout=10) as response:
        # 腾讯使用 GBK 编码
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
                'yesterday_close': fields[4] if len(fields) > 4 else '',
                'open': fields[5] if len(fields) > 5 else '',
                'volume': fields[6] if len(fields) > 6 else '',
                'change': fields[31] if len(fields) > 31 else '',
                'change_percent': fields[32] if len(fields) > 32 else '',
                'high': fields[33] if len(fields) > 33 else '',
                'low': fields[34] if len(fields) > 34 else '',
                'time': fields[30] if len(fields) > 30 else '',
            }
    return result

def format_stock_info(stock):
    """格式化股票信息"""
    name = stock.get('name', '')
    code = stock.get('code', '')
    price = stock.get('price', '')
    change = stock.get('change', '')
    change_pct = stock.get('change_percent', '')
    high = stock.get('high', '')
    low = stock.get('low', '')
    
    # 判断涨跌
    try:
        change_val = float(change) if change else 0
        emoji = '📈' if change_val >= 0 else '📉'
        sign = '+' if change_val >= 0 else ''
    except:
        emoji = '➖'
        sign = ''
    
    return f"{emoji} {name} ({code})\n  现价: {price}\n  涨跌: {sign}{change} ({sign}{change_pct}%)\n  最高: {high} / 最低: {low}"

if __name__ == '__main__':
    # 默认查询：恒生指数、腾讯、阿里
    stocks = get_hk_stock(['HSI', '00700', '09988'])
    
    for code, info in stocks.items():
        print(format_stock_info(info))
        print()
