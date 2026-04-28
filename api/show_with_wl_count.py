#!/usr/bin/env python3
"""
展示数据 - 包含波长数量计算
"""

import sqlite3
import re
from datetime import datetime

DB_PATH = '/Users/rocky/.openclaw/workspace/transmission_resource.db'


def get_wavelength_count(card_type):
    """根据板卡类型计算波长数量"""
    if not card_type:
        return 0
    
    card_type = str(card_type).upper()
    
    # 华为板卡
    if 'N2MD02' in card_type:
        return 2  # N2MD02 支持 2 个波长
    elif 'N2MS04' in card_type:
        return 1  # N2MS04 支持 1 个波长
    elif 'N2MD04CE' in card_type:
        return 2  # N2MD04CE 支持 2 个波长
    
    # ACCESSLINK/光迅板卡
    elif 'T1X200S' in card_type.upper():
        return 1  # T1X200S 支持 1 个波长
    elif 'T04X1-103' in card_type.upper() or 'T04X1' in card_type.upper():
        return 1  # T04X1-103 支持 1 个波长
    
    return 0


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
        # 从description中提取波长
        wavelengths = []
        direction = '-'
        
        if row['description']:
            # 提取所有波长
            wl_matches = re.findall(r'波长:(\d{3}\.\d)', row['description'])
            wavelengths = [wl + 'nm' for wl in wl_matches]
            
            # 提取方向
            dir_match = re.search(r'方向:([^\s]+)', row['description'])
            if dir_match:
                direction = dir_match.group(1)
        
        # 计算波长数量
        wl_count = get_wavelength_count(row['card_type'])
        
        # 构建波长显示字符串
        if wavelengths:
            wl_display = ', '.join(wavelengths)
        else:
            wl_display = '-'
        
        results.append({
            'device_name': row['device_name'],
            'vendor': row['vendor'],
            'device_type': row['device_type'],
            'slot': row['slot_number'],
            'card_type': row['card_type'] or '-',
            'status': '在用' if row['status'] == 'active' else '空置',
            'wl_count': wl_count,
            'wavelengths': wl_display,
            'direction': direction
        })
    
    conn.close()
    return results


def generate_html():
    """生成HTML报告"""
    
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
        .wl-count {{
            display: inline-block;
            background: #52c41a;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        .wl-count-0 {{
            background: #d9d9d9;
        }}
        .wl-count-1 {{
            background: #1890ff;
        }}
        .wl-count-2 {{
            background: #52c41a;
        }}
        .device-name {{
            font-weight: 500;
            color: #333;
        }}
        .card-type {{
            font-family: monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 传输资源数据展示</h1>
        <p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 波长数量根据板卡类型计算</p>
        
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
                        <th>波长数量</th>
                        <th>波长</th>
                        <th>方向</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
'''
    
    for row in yunlifang_data:
        vendor_class = ''
        if row['vendor'] == 'HUAWEI':
            vendor_class = 'vendor-huawei'
        elif row['vendor'] == 'ACCESSLINK':
            vendor_class = 'vendor-accesslink'
        
        status_class = 'status-active' if row['status'] == '在用' else 'status-empty'
        wl_count_class = f'wl-count wl-count-{row["wl_count"]}'
        
        html += f'''
                    <tr class="{vendor_class}">
                        <td>{row['vendor']}</td>
                        <td>{row['device_type']}</td>
                        <td class="device-name">{row['device_name']}</td>
                        <td>{row['slot']}</td>
                        <td class="card-type">{row['card_type']}</td>
                        <td><span class="{wl_count_class}">{row['wl_count']}</span></td>
                        <td class="wavelength">{row['wavelengths']}</td>
                        <td>{row['direction']}</td>
                        <td class="{status_class}">{row['status']}</td>
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
                        <th>波长数量</th>
                        <th>波长</th>
                        <th>方向</th>
                        <th>状态</th>
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
        wl_count_class = f'wl-count wl-count-{row["wl_count"]}'
        
        html += f'''
                    <tr class="{vendor_class}">
                        <td>{row['vendor']}</td>
                        <td>{row['device_type']}</td>
                        <td class="device-name">{row['device_name']}</td>
                        <td>{row['slot']}</td>
                        <td class="card-type">{row['card_type']}</td>
                        <td><span class="{wl_count_class}">{row['wl_count']}</span></td>
                        <td class="wavelength">{row['wavelengths']}</td>
                        <td>{row['direction']}</td>
                        <td class="{status_class}">{row['status']}</td>
                    </tr>
'''
    
    html += '''
                </tbody>
            </table>
        </div>
        
        <div class="site-section">
            <div class="site-title">📋 板卡波长容量说明</div>
            <table>
                <thead>
                    <tr>
                        <th>厂商</th>
                        <th>板卡型号</th>
                        <th>波长数量</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="vendor-huawei">
                        <td>HUAWEI</td>
                        <td class="card-type">N2MD02</td>
                        <td><span class="wl-count wl-count-2">2</span></td>
                        <td>双波长板卡</td>
                    </tr>
                    <tr class="vendor-huawei">
                        <td>HUAWEI</td>
                        <td class="card-type">N2MS04</td>
                        <td><span class="wl-count wl-count-1">1</span></td>
                        <td>单波长板卡</td>
                    </tr>
                    <tr class="vendor-huawei">
                        <td>HUAWEI</td>
                        <td class="card-type">N2MD04CE</td>
                        <td><span class="wl-count wl-count-2">2</span></td>
                        <td>双波长板卡</td>
                    </tr>
                    <tr class="vendor-accesslink">
                        <td>ACCESSLINK</td>
                        <td class="card-type">T1X200S</td>
                        <td><span class="wl-count wl-count-1">1</span></td>
                        <td>单波长板卡</td>
                    </tr>
                    <tr class="vendor-accesslink">
                        <td>ACCESSLINK</td>
                        <td class="card-type">T04X1-103</td>
                        <td><span class="wl-count wl-count-1">1</span></td>
                        <td>单波长板卡</td>
                    </tr>
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
    output_path = '/Users/rocky/.openclaw/workspace/frontend/resource_wl_count.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"报告已生成: {output_path}")
