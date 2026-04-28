#!/usr/bin/env python3
"""
简单展示 - 按Excel格式展示数据
"""

import sqlite3
from datetime import datetime

DB_PATH = '/Users/rocky/.openclaw/workspace/transmission_resource.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_site_data(site_name):
    """获取机房数据"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            d.name as device_name,
            d.vendor,
            d.device_type,
            c.slot_number,
            c.card_type,
            c.status,
            c.description
        FROM devices d
        LEFT JOIN cards c ON d.id = c.device_id
        WHERE d.site_id = (SELECT id FROM sites WHERE name = ?)
        ORDER BY d.vendor, d.name, c.slot_number
    ''', (site_name,))
    
    results = []
    for row in cursor.fetchall():
        # 从description中提取波长和方向
        wavelength = '-'
        direction = '-'
        usage = '-'
        
        if row['description']:
            import re
            # 提取波长
            wl_match = re.search(r'波长:(\d{3}\.\d)', row['description'])
            if wl_match:
                wavelength = wl_match.group(1) + 'nm'
            
            # 提取方向
            dir_match = re.search(r'方向:([^\s]+)', row['description'])
            if dir_match:
                direction = dir_match.group(1)
            
            # 提取详情（去掉波长和方向前缀）
            usage = row['description']
            # 简化显示，只保留核心信息
            if '详情:' in usage:
                usage = usage.split('详情:')[-1][:50]
        
        results.append({
            'device_name': row['device_name'],
            'vendor': row['vendor'],
            'device_type': row['device_type'],
            'slot': row['slot_number'],
            'card_type': row['card_type'] or '-',
            'status': '在用' if row['status'] == 'active' else '空置',
            'wavelength': wavelength,
            'direction': direction,
            'usage': usage
        })
    
    conn.close()
    return results


def generate_html():
    """生成简单HTML报告"""
    
    yunlifang_data = get_site_data('云立方机房')
    jiading_data = get_site_data('嘉定机房')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>传输资源数据展示</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f7fa;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .site-section {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .site-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e8e8e8;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 8px;
            text-align: left;
            border: 1px solid #e8e8e8;
        }}
        th {{
            background: #fafafa;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        tr:hover {{
            background: #f5f7fa;
        }}
        .vendor-huawei {{
            background: #e6f7ff;
        }}
        .vendor-accesslink {{
            background: #fff7e6;
        }}
        .status-active {{
            color: #52c41a;
            font-weight: bold;
        }}
        .status-empty {{
            color: #999;
        }}
        .wavelength {{
            font-family: monospace;
            color: #1890ff;
            font-weight: 500;
        }}
        .device-name {{
            font-weight: 500;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 传输资源数据展示</h1>
        <p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="site-section">
            <div class="site-title">🏢 云立方机房业务板使用情况</div>
            <table>
                <thead>
                    <tr>
                        <th>设备品牌</th>
                        <th>设备型号</th>
                        <th>设备编号</th>
                        <th>槽位</th>
                        <th>板卡型号</th>
                        <th>使用状况</th>
                        <th>波长</th>
                        <th>方向</th>
                    </tr>
                </thead>
                <tbody>
'''
    
    current_vendor = None
    for row in yunlifang_data:
        vendor_class = ''
        if row['vendor'] == 'HUAWEI':
            vendor_class = 'vendor-huawei'
        elif row['vendor'] == 'ACCESSLINK':
            vendor_class = 'vendor-accesslink'
        
        status_class = 'status-active' if row['status'] == '在用' else 'status-empty'
        
        html += f'''
                    <tr class="{vendor_class}">
                        <td>{row['vendor']}</td>
                        <td>{row['device_type']}</td>
                        <td class="device-name">{row['device_name']}</td>
                        <td>{row['slot']}</td>
                        <td>{row['card_type']}</td>
                        <td class="{status_class}">{row['status']}</td>
                        <td class="wavelength">{row['wavelength']}</td>
                        <td>{row['direction']}</td>
                    </tr>
'''
    
    html += '''
                </tbody>
            </table>
        </div>
        
        <div class="site-section">
            <div class="site-title">🏢 嘉定机房业务板使用情况</div>
            <table>
                <thead>
                    <tr>
                        <th>设备品牌</th>
                        <th>设备型号</th>
                        <th>设备编号</th>
                        <th>槽位</th>
                        <th>板卡型号</th>
                        <th>使用状况</th>
                        <th>波长</th>
                        <th>方向</th>
                    </tr>
                </thead>
                <tbody>
'''
    
    for row in jiading_data:
        vendor_class = ''
        if row['vendor'] == 'HUAWEI':
            vendor_class = 'vendor-huawei'
        elif row['vendor'] == 'ACCESSLINK':
            vendor_class = 'vendor-accesslink'
        
        status_class = 'status-active' if row['status'] == '在用' else 'status-empty'
        
        html += f'''
                    <tr class="{vendor_class}">
                        <td>{row['vendor']}</td>
                        <td>{row['device_type']}</td>
                        <td class="device-name">{row['device_name']}</td>
                        <td>{row['slot']}</td>
                        <td>{row['card_type']}</td>
                        <td class="{status_class}">{row['status']}</td>
                        <td class="wavelength">{row['wavelength']}</td>
                        <td>{row['direction']}</td>
                    </tr>
'''
    
    html += '''
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
'''
    
    return html


if __name__ == '__main__':
    html = generate_html()
    output_path = '/Users/rocky/.openclaw/workspace/frontend/resource_simple.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"简单报告已生成: {output_path}")
