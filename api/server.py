#!/usr/bin/env python3
"""
传输资源管理平台 - API服务
"""
import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'transmission_resource.db')
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 简化日志输出
        pass
    
    def do_GET(self):
        path = self.path
        
        # API路由
        if path == '/api/boards':
            self.handle_get_boards()
        elif path == '/api/wavelengths':
            self.handle_get_wavelengths()
        elif path == '/api/stats':
            self.handle_get_stats()
        # 静态文件服务
        elif path == '/' or path == '/index.html':
            self.serve_file('board_view.html')
        elif path.startswith('/'):
            file_path = path[1:]  # 去掉开头的/
            self.serve_file(file_path)
        else:
            self.send_error(404)
    
    def handle_get_boards(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, room_name, device_brand, device_model, device_code, 
                       slot, board_model, usage_status
                FROM business_boards
                ORDER BY room_name, device_code, slot
            ''')
            
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]
            conn.close()
            
            self.send_json_response({'success': True, 'data': data, 'total': len(data)})
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_get_wavelengths(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, sheet_name, plane, local_network_device, local_network_port,
                       a_transmission_device, wavelength, z_transmission_device,
                       remote_room_device, remark
                FROM wavelength_connections
                ORDER BY sheet_name, wavelength
            ''')
            
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]
            conn.close()
            
            self.send_json_response({'success': True, 'data': data, 'total': len(data)})
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_get_stats(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # 各机房统计
            cursor.execute('''
                SELECT room_name, COUNT(*) as count 
                FROM business_boards 
                GROUP BY room_name
            ''')
            room_stats = {row[0]: row[1] for row in cursor.fetchall()}
            
            # 总记录数
            cursor.execute('SELECT COUNT(*) FROM business_boards')
            total = cursor.fetchone()[0]
            
            # 波长连接统计
            cursor.execute('SELECT COUNT(*) FROM wavelength_connections')
            wavelength_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT sheet_name, COUNT(*) as count FROM wavelength_connections GROUP BY sheet_name')
            wavelength_sheets = {row[0]: row[1] for row in cursor.fetchall()}
            
            conn.close()
            
            self.send_json_response({
                'success': True,
                'total': total,
                'rooms': room_stats,
                'wavelength_count': wavelength_count,
                'wavelength_sheets': wavelength_sheets
            })
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_file(self, filename):
        filepath = os.path.join(FRONTEND_PATH, filename)
        if not os.path.exists(filepath):
            filepath = os.path.join(FRONTEND_PATH, 'board_view.html')
        
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # 根据扩展名设置Content-Type
            if filename.endswith('.html'):
                content_type = 'text/html'
            elif filename.endswith('.js'):
                content_type = 'application/javascript'
            elif filename.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))
    
    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def run_server(port=8888):
    server = HTTPServer(('127.0.0.1', port), APIHandler)
    print(f"🚀 服务器启动: http://localhost:{port}")
    print(f"📊 数据库: {DB_PATH}")
    print("按 Ctrl+C 停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")

if __name__ == '__main__':
    run_server()
