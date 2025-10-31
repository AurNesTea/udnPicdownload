#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端錯誤日誌接收伺服器
接收前端發送的錯誤日誌並寫入 logs/front_logs 檔案
"""

import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# 設定路徑
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
LOG_FILE = os.path.join(REPO_ROOT, 'logs', 'front_logs.log')

# 確保 logs 目錄存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


class LogHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/log-front-error':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                log_entry = json.loads(post_data.decode('utf-8'))
                
                # 格式化日誌條目（類似 update_data.log 的格式）
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_line = f"{timestamp} - ERROR - [{log_entry.get('file', 'unknown')}] {log_entry.get('message', '')} | URL: {log_entry.get('url', '')} | UserAgent: {log_entry.get('userAgent', '')[:100]}\n"
                
                # 寫入日誌檔案（追加模式）
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(log_line)
                
                # 回應成功
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                
                print(f"✓ 已記錄前端錯誤: {log_entry.get('message', '')}")
                
            except Exception as e:
                print(f"✗ 處理日誌錯誤: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # 處理 CORS preflight 請求
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # 覆蓋預設的日誌輸出，避免過多訊息
        pass


def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, LogHandler)
    print(f"前端日誌伺服器已啟動，監聽埠號: {port}")
    print(f"日誌檔案位置: {LOG_FILE}")
    print("按 Ctrl+C 停止伺服器")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止")
        httpd.server_close()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(port)

