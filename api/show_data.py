#!/usr/bin/env python3
"""
读取数据库并生成HTML报告
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = '/Users/rocky/.openclaw/workspace/transmission_resource.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_sites_summary():
    """获取各机房汇总数据"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            s.name as site_name,
            COUNT(DISTINCT d.id) as device_count,
            COUNT(c.id) as total_slots,
            SUM(CASE WHEN c.status = 'active' THEN 1 ELSE 0 END) as active_slots
        FROM sites s
        LEFT JOIN devices d ON s.id = d.site_id
        LEFT JOIN cards c ON d.id = c.device_id
        GROUP BY s.id, s.name
    ''')
    
    sites = []
    for row in cursor.fetchall():
        sites.append({
            'name': row['site_name'],
            'devices': row['device_count'],
            'total_slots': row['total_slots'] or 0,
            'active_slots': row['active_slots'] or 0,
            'utilization': round((row['active_slots'] or 0) / (row['total_slots'] or 1) * 100, 1) if row['total_slots'] else 0
        })
    
    conn.close()
    return sites

def get_site_detail(site_name):
    """获取机房详细数据"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取设备和板卡
    cursor.execute('''
        SELECT 
            d.id as device_id,
            d.name as device_name,
            d.device_code,
            d.vendor,
            d.device_type,
            c.id as card_id,
            c.slot_number,
            c.card_type,
            c.status,
            c.description
        FROM devices d
        LEFT JOIN cards c ON d.id = c.device_id
        WHERE d.site_id = (SELECT id FROM sites WHERE name = ?)
        ORDER BY d.vendor, d.name, c.slot_number
    ''', (site_name,))
    
    devices = {}
    for row in cursor.fetchall():
        device_id = row['device_id']
        if device_id not in devices:
            devices[device_id] = {
                'id': device_id,
                'name': row['device_name'],
                'code': row['device_code'],
                'vendor': row['vendor'],
                'type': row['device_type'],
                'cards': []
            }
        
        if row['card_id']:
            wavelength = None
            direction = None
            if row['description']:
                import re
                wl_match = re.search(r'波长:(\d{3}\.\d)', row['description'])
                if wl_match:
                    wavelength = wl_match.group(1)
                dir_match = re.search(r'方向:([^\s]+)', row['description'])
                if dir_match:
                    direction = dir_match.group(1)
            
            devices[device_id]['cards'].append({
                'slot': row['slot_number'],
                'type': row['card_type'],
                'status': row['status'],
                'wavelength': wavelength,
                'direction': direction,
                'description': row['description']
            })
    
    conn.close()
    return list(devices.values())

def get_wavelength_stats():
    """获取波长统计"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.description, s.name as site_name
        FROM cards c
        JOIN devices d ON c.device_id = d.id
        JOIN sites s ON d.site_id = s.id
        WHERE c.status = 'active' AND c.description LIKE '%波长:%'
    ''')
    
    import re
    wavelengths = {}
    for row in cursor.fetchall():
        desc = row['description']
        site = row['site_name']
        match = re.search(r'波长:(\d{3}\.\d)', desc)
        if match:
            wl = match.group(1)
            if wl not in wavelengths:
                wavelengths[wl] = {'count': 0, 'sites': set()}
            wavelengths[wl]['count'] += 1
            wavelengths[wl]['sites'].add(site)
    
    # 转换为列表并排序
    result = []
    for wl, data in sorted(wavelengths.items(), key=lambda x: float(x[0])):
        result.append({
            'wavelength': wl,
            'count': data['count'],
            'sites': list(data['sites'])
        })
    
    conn.close()
    return result


def get_wavelength_stats_by_vendor(site_name, vendor):
    """按厂商获取波长统计"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.description
        FROM cards c
        JOIN devices d ON c.device_id = d.id
        JOIN sites s ON d.site_id = s.id
        WHERE s.name = ? AND d.vendor = ? AND c.status = 'active' AND c.description LIKE '%波长:%'
    ''', (site_name, vendor))
    
    import re
    wavelengths = {}
    for row in cursor.fetchall():
        desc = row['description']
        match = re.search(r'波长:(\d{3}\.\d)', desc)
        if match:
            wl = match.group(1)
            wavelengths[wl] = wavelengths.get(wl, 0) + 1
    
    # 转换为列表并排序
    result = []
    for wl, count in sorted(wavelengths.items(), key=lambda x: float(x[0])):
        result.append({'wavelength': wl, 'count': count})
    
    conn.close()
    return result

def generate_html():
    """生成HTML报告"""
    sites = get_sites_summary()
    
    # 获取每个机房的详细数据
    yunlifang_devices = get_site_detail('云立方机房')
    jiading_devices = get_site_detail('嘉定机房')
    
    # 按平面获取波长统计
    yunlifang_huawei_wl = get_wavelength_stats_by_vendor('云立方机房', 'HUAWEI')
    yunlifang_accesslink_wl = get_wavelength_stats_by_vendor('云立方机房', 'ACCESSLINK')
    jiading_huawei_wl = get_wavelength_stats_by_vendor('嘉定机房', 'HUAWEI')
    jiading_accesslink_wl = get_wavelength_stats_by_vendor('嘉定机房', 'ACCESSLINK')
    
    total_devices = sum(s['devices'] for s in sites)
    total_slots = sum(s['total_slots'] for s in sites)
    total_active = sum(s['active_slots'] for s in sites)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>传输资源数据查看</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f7fa;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #1a1a1a;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #666;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #1890ff;
        }}
        .site-section {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .site-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e8e8e8;
        }}
        .site-title {{
            font-size: 20px;
            font-weight: bold;
            color: #1a1a1a;
        }}
        .site-stats {{
            font-size: 14px;
            color: #666;
        }}
        .vendor-group {{
            margin-bottom: 20px;
        }}
        .vendor-title {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            padding: 5px 10px;
            background: #f0f0f0;
            border-radius: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #e8e8e8;
        }}
        th {{
            background: #fafafa;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f5f7fa;
        }}
        .status-active {{
            color: #52c41a;
            font-weight: bold;
        }}
        .status-empty {{
            color: #999;
        }}
        .wavelength {{
            background: #1890ff;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}
        .direction {{
            color: #666;
            font-size: 12px;
        }}
        .warning {{
            background: #fff2f0;
            border: 1px solid #ffccc7;
            padding: 10px;
            border-radius: 4px;
            color: #cf1322;
            margin-bottom: 20px;
        }}
        .success {{
            background: #f6ffed;
            border: 1px solid #b7eb8f;
            padding: 10px;
            border-radius: 4px;
            color: #389e0d;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 传输资源数据查看</h1>
        <p style="text-align: center; color: #666;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>总设备数</h3>
                <div class="stat-value">{total_devices}</div>
            </div>
            <div class="stat-card">
                <h3>总槽位数</h3>
                <div class="stat-value">{total_slots}</div>
            </div>
            <div class="stat-card">
                <h3>在用槽位</h3>
                <div class="stat-value">{total_active}</div>
            </div>
            <div class="stat-card">
                <h3>总体利用率</h3>
                <div class="stat-value">{round(total_active/total_slots*100, 1) if total_slots else 0}%</div>
            </div>
        </div>
'''
    
    # 添加各机房数据
    for site in sites:
        html += f'''
        <div class="site-section">
            <div class="site-header">
                <div class="site-title">🏢 {site['name']}</div>
                <div class="site-stats">
                    设备: {site['devices']} 台 | 
                    槽位: {site['active_slots']}/{site['total_slots']} | 
                    利用率: {site['utilization']}%
                </div>
            </div>
'''
        
        # 获取该机房详细数据
        devices = yunlifang_devices if site['name'] == '云立方机房' else jiading_devices
        
        # 按厂商分组
        vendors = {}
        for device in devices:
            vendor = device['vendor'] or '未知'
            if vendor not in vendors:
                vendors[vendor] = []
            vendors[vendor].append(device)
        
        for vendor, vendor_devices in vendors.items():
            html += f'''
            <div class="vendor-group">
                <div class="vendor-title">{vendor} ({len(vendor_devices)} 台设备)</div>
                <table>
                    <thead>
                        <tr>
                            <th>设备名称</th>
                            <th>型号</th>
                            <th>槽位</th>
                            <th>板卡类型</th>
                            <th>状态</th>
                            <th>波长</th>
                            <th>方向</th>
                        </tr>
                    </thead>
                    <tbody>
'''
            for device in vendor_devices:
                for card in device['cards']:
                    status_class = 'status-active' if card['status'] == 'active' else 'status-empty'
                    status_text = '在用' if card['status'] == 'active' else '空置'
                    wavelength_html = f'<span class="wavelength">{card["wavelength"]}nm</span>' if card['wavelength'] else '-'
                    direction_html = f'<span class="direction">{card["direction"]}</span>' if card['direction'] else '-'
                    
                    html += f'''
                        <tr>
                            <td>{device['name']}</td>
                            <td>{device['type']}</td>
                            <td>{card['slot']}</td>
                            <td>{card['type'] or '-'}</td>
                            <td class="{status_class}">{status_text}</td>
                            <td>{wavelength_html}</td>
                            <td>{direction_html}</td>
                        </tr>
'''
            
            html += '''
                    </tbody>
                </table>
            </div>
'''
        
        html += '</div>'
    
    # 添加波长统计 - 按平面分开展示
    html += '''
        <div class="site-section">
            <div class="site-header">
                <div class="site-title">📡 波长使用统计（按平面分组）</div>
            </div>
            
            <div class="vendor-group">
                <div class="vendor-title huawei">🏢 云立方机房 - HUAWEI 平面</div>
                <table>
                    <thead>
                        <tr>
                            <th>波长</th>
                            <th>使用次数</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    for wl in yunlifang_huawei_wl:
        html += f'''
                        <tr>
                            <td><span class="wavelength">{wl['wavelength']}nm</span></td>
                            <td>{wl['count']}</td>
                        </tr>
'''
    if not yunlifang_huawei_wl:
        html += '<tr><td colspan="2" style="text-align: center; color: #999;">无波长数据</td></tr>'
    
    html += '''
                    </tbody>
                </table>
            </div>
            
            <div class="vendor-group">
                <div class="vendor-title guangxun">🏢 云立方机房 - ACCESSLINK 平面</div>
                <table>
                    <thead>
                        <tr>
                            <th>波长</th>
                            <th>使用次数</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    for wl in yunlifang_accesslink_wl:
        html += f'''
                        <tr>
                            <td><span class="wavelength">{wl['wavelength']}nm</span></td>
                            <td>{wl['count']}</td>
                        </tr>
'''
    if not yunlifang_accesslink_wl:
        html += '<tr><td colspan="2" style="text-align: center; color: #999;">无波长数据</td></tr>'
    
    html += '''
                    </tbody>
                </table>
            </div>
            
            <div class="vendor-group">
                <div class="vendor-title huawei">🏢 嘉定机房 - HUAWEI 平面</div>
                <table>
                    <thead>
                        <tr>
                            <th>波长</th>
                            <th>使用次数</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    for wl in jiading_huawei_wl:
        html += f'''
                        <tr>
                            <td><span class="wavelength">{wl['wavelength']}nm</span></td>
                            <td>{wl['count']}</td>
                        </tr>
'''
    if not jiading_huawei_wl:
        html += '<tr><td colspan="2" style="text-align: center; color: #999;">无波长数据</td></tr>'
    
    html += '''
                    </tbody>
                </table>
            </div>
            
            <div class="vendor-group">
                <div class="vendor-title guangxun">🏢 嘉定机房 - ACCESSLINK 平面</div>
                <table>
                    <thead>
                        <tr>
                            <th>波长</th>
                            <th>使用次数</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    for wl in jiading_accesslink_wl:
        html += f'''
                        <tr>
                            <td><span class="wavelength">{wl['wavelength']}nm</span></td>
                            <td>{wl['count']}</td>
                        </tr>
'''
    if not jiading_accesslink_wl:
        html += '<tr><td colspan="2" style="text-align: center; color: #999;">无波长数据</td></tr>'
    
    html += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    return html

if __name__ == '__main__':
    html = generate_html()
    output_path = '/Users/rocky/.openclaw/workspace/frontend/resource_report.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"报告已生成: {output_path}")
