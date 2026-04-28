#!/usr/bin/env python3
"""
港股 K 线图网页生成器 - 使用 TradingView 的 Lightweight Charts
"""
import urllib.request
import json
from datetime import datetime, timedelta
import os

def get_hk_kline(code, days=30):
    """获取港股 K 线数据"""
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
                parts = line.split(',')
                # 转换日期格式为时间戳
                date_str = parts[0]
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                timestamp = int(dt.timestamp())
                
                klines.append({
                    'time': timestamp,
                    'open': float(parts[1]),
                    'high': float(parts[3]),
                    'low': float(parts[4]),
                    'close': float(parts[2]),
                })
        return klines, data.get('data', {}).get('name', code)
    except Exception as e:
        print(f"获取数据失败: {e}")
        return [], code

def create_kline_html(code, output_path):
    """生成带 K 线图的 HTML"""
    klines, name = get_hk_kline(code, days=30)
    
    if not klines:
        print("没有数据")
        return
    
    # 转换为 JSON
    chart_data = json.dumps(klines)
    
    # 计算最新价格信息
    latest = klines[-1]
    prev = klines[-2] if len(klines) > 1 else klines[-1]
    change = latest['close'] - prev['close']
    change_pct = (change / prev['close']) * 100 if prev['close'] else 0
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{name} K线图</title>
    <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0d1117;
            color: #fff;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .price-info {{
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 18px;
        }}
        .price {{ font-weight: bold; font-size: 28px; }}
        .up {{ color: #00d26a; }}
        .down {{ color: #ff4757; }}
        #chart {{
            width: 100%;
            height: 500px;
            border-radius: 12px;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 {name} ({code})</h1>
        <div class="price-info">
            <span class="price {'up' if change >= 0 else 'down'}">{latest['close']:.2f}</span>
            <span class="{'up' if change >= 0 else 'down'}">{change:+.2f} ({change_pct:+.2f}%)</span>
        </div>
    </div>
    <div id="chart"></div>
    
    <script>
        const chartData = {chart_data};
        
        const chart = LightweightCharts.createChart(document.getElementById('chart'), {{
            layout: {{
                background: {{ color: '#0d1117' }},
                textColor: '#d1d5db',
            }},
            grid: {{
                vertLines: {{ color: '#21262d' }},
                horzLines: {{ color: '#21262d' }},
            }},
            crosshair: {{
                mode: LightweightCharts.CrosshairMode.Normal,
            }},
            rightPriceScale: {{
                borderColor: '#30363d',
            }},
            timeScale: {{
                borderColor: '#30363d',
                timeVisible: false,
            }},
        }});
        
        const candleSeries = chart.addCandlestickSeries({{
            upColor: '#00d26a',
            downColor: '#ff4757',
            borderUpColor: '#00d26a',
            borderDownColor: '#ff4757',
            wickUpColor: '#00d26a',
            wickDownColor: '#ff4757',
        }});
        
        candleSeries.setData(chartData);
        chart.timeScale().fitContent();
    </script>
</body>
</html>
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"K线图网页已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else 'HSI'
    output = os.path.expanduser('~/.openclaw/workspace/tools/hkstock/kline_chart.html')
    create_kline_html(code, output)
