#!/usr/bin/env python3
"""
创建传输资源互联拓扑图
"""

import sqlite3
import re
from datetime import datetime

DB_PATH = '/Users/rocky/.openclaw/workspace/transmission_resource.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def parse_connection(description):
    """从描述中解析连接信息"""
    if not description:
        return None
    
    # 提取方向信息
    directions = []
    if '云立方' in description:
        directions.append('云立方')
    if '常熟' in description:
        directions.append('常熟')
    if '嘉定' in description:
        directions.append('嘉定')
    if '吴江' in description:
        directions.append('吴江')
    if '腾讯' in description:
        directions.append('腾讯')
    if '外高桥' in description:
        directions.append('外高桥')
    if '苏州' in description:
        directions.append('苏州')
    
    # 提取波长
    wl_match = re.search(r'(\d{3}\.\d)', description)
    wavelength = wl_match.group(1) if wl_match else None
    
    return {
        'directions': directions,
        'wavelength': wavelength,
        'raw': description[:60]
    }


def get_all_connections():
    """获取所有连接信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            s.name as site_name,
            d.name as device_name,
            d.vendor,
            d.device_type,
            c.slot_number,
            c.card_type,
            c.description
        FROM cards c
        JOIN devices d ON c.device_id = d.id
        JOIN sites s ON d.site_id = s.id
        WHERE c.status = 'active' AND c.description IS NOT NULL
        ORDER BY s.name, d.vendor, d.name, c.slot_number
    ''')
    
    connections = []
    for row in cursor.fetchall():
        conn_info = parse_connection(row['description'])
        if conn_info and conn_info['directions']:
            connections.append({
                'site': row['site_name'],
                'device': row['device_name'],
                'vendor': row['vendor'],
                'type': row['device_type'],
                'slot': row['slot_number'],
                'card': row['card_type'],
                'directions': conn_info['directions'],
                'wavelength': conn_info['wavelength'],
                'raw': conn_info['raw']
            })
    
    conn.close()
    return connections


def analyze_topology(connections):
    """分析拓扑结构"""
    # 按机房分组
    sites = {}
    for conn in connections:
        site = conn['site']
        if site not in sites:
            sites[site] = {
                'devices': {},
                'connections': []
            }
        
        device = conn['device']
        if device not in sites[site]['devices']:
            sites[site]['devices'][device] = {
                'vendor': conn['vendor'],
                'type': conn['type'],
                'slots': []
            }
        
        sites[site]['devices'][device]['slots'].append({
            'slot': conn['slot'],
            'card': conn['card'],
            'directions': conn['directions'],
            'wavelength': conn['wavelength']
        })
        
        # 记录连接关系
        for direction in conn['directions']:
            if direction != site.replace('机房', ''):  # 排除本机房
                sites[site]['connections'].append({
                    'from_device': device,
                    'to_site': direction,
                    'wavelength': conn['wavelength']
                })
    
    return sites


def generate_html():
    """生成拓扑图HTML"""
    connections = get_all_connections()
    topology = analyze_topology(connections)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>传输资源互联拓扑图</title>
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
        .topology-container {{
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }}
        .site-box {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            min-width: 280px;
            max-width: 350px;
        }}
        .site-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e8e8e8;
            text-align: center;
        }}
        .device-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .device-item {{
            background: #f5f7fa;
            padding: 10px 12px;
            border-radius: 6px;
            border-left: 3px solid #1890ff;
        }}
        .device-item.huawei {{
            border-left-color: #1890ff;
            background: #e6f7ff;
        }}
        .device-item.accesslink {{
            border-left-color: #fa8c16;
            background: #fff7e6;
        }}
        .device-name {{
            font-weight: 600;
            font-size: 13px;
            color: #333;
            margin-bottom: 4px;
        }}
        .device-info {{
            font-size: 11px;
            color: #666;
        }}
        .connections {{
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px dashed #d9d9d9;
        }}
        .connection-tag {{
            display: inline-block;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            margin: 2px;
        }}
        .conn-yunlifang {{
            background: #52c41a;
            color: white;
        }}
        .conn-changshu {{
            background: #722ed1;
            color: white;
        }}
        .conn-jiading {{
            background: #fa541c;
            color: white;
        }}
        .conn-wujiang {{
            background: #13c2c2;
            color: white;
        }}
        .conn-tengxun {{
            background: #eb2f96;
            color: white;
        }}
        .wavelength {{
            font-family: monospace;
            font-size: 10px;
            opacity: 0.9;
        }}
        .legend {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .legend-title {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .legend-items {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }}
        .detail-section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .detail-title {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border: 1px solid #e8e8e8;
        }}
        th {{
            background: #fafafa;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f5f7fa;
        }}
        .arrow-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 传输资源互联拓扑图</h1>
        <p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="legend">
            <div class="legend-title">图例说明</div>
            <div class="legend-items">
                <div class="legend-item">
                    <div class="legend-color" style="background: #1890ff;"></div>
                    <span>HUAWEI 设备</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #fa8c16;"></div>
                    <span>ACCESSLINK 设备</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color conn-yunlifang"></div>
                    <span>云立方方向</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color conn-changshu"></div>
                    <span>常熟方向</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color conn-jiading"></div>
                    <span>嘉定方向</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color conn-wujiang"></div>
                    <span>吴江方向</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color conn-tengxun"></div>
                    <span>腾讯方向</span>
                </div>
            </div>
        </div>
'''
    
    # 生成拓扑图
    html += '<div class="topology-container">'
    
    for site_name, site_data in topology.items():
        html += f'''
        <div class="site-box">
            <div class="site-title">🏢 {site_name}</div>
            <div class="device-list">
'''
        
        # 按厂商分组显示设备
        for device_name, device_info in site_data['devices'].items():
            vendor_class = 'huawei' if device_info['vendor'] == 'HUAWEI' else 'accesslink'
            
            # 统计连接
            conn_tags = []
            for slot in device_info['slots']:
                for direction in slot['directions']:
                    wl = slot['wavelength'] or ''
                    direction_class = 'conn-yunlifang'
                    if '常熟' in direction:
                        direction_class = 'conn-changshu'
                    elif '嘉定' in direction:
                        direction_class = 'conn-jiading'
                    elif '吴江' in direction:
                        direction_class = 'conn-wujiang'
                    elif '腾讯' in direction:
                        direction_class = 'conn-tengxun'
                    
                    tag = f'<span class="connection-tag {direction_class}">{direction} <span class="wavelength">{wl}</span></span>'
                    if tag not in conn_tags:
                        conn_tags.append(tag)
            
            html += f'''
                <div class="device-item {vendor_class}">
                    <div class="device-name">{device_name}</div>
                    <div class="device-info">{device_info['vendor']} {device_info['type']} | {len(device_info['slots'])} 槽位</div>
                    <div class="connections">{''.join(conn_tags[:5])}</div>
                </div>
'''
        
        html += '''
            </div>
        </div>
'''
    
    html += '</div>'
    
    # 添加详细连接表
    html += '''
        <div class="detail-section">
            <div class="detail-title">📋 详细连接列表</div>
            <table>
                <thead>
                    <tr>
                        <th>源机房</th>
                        <th>源设备</th>
                        <th>槽位</th>
                        <th>板卡</th>
                        <th>目标方向</th>
                        <th>波长</th>
                    </tr>
                </thead>
                <tbody>
'''
    
    for conn in connections:
        for direction in conn['directions']:
            html += f'''
                    <tr>
                        <td>{conn['site']}</td>
                        <td>{conn['device']}</td>
                        <td>{conn['slot']}</td>
                        <td>{conn['card']}</td>
                        <td>{direction}</td>
                        <td class="wavelength">{conn['wavelength'] or '-'}</td>
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
    output_path = '/Users/rocky/.openclaw/workspace/frontend/topology.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"拓扑图已生成: {output_path}")
