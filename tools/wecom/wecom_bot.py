#!/usr/bin/env python3
"""
企业微信机器人消息发送
用法: python3 wecom_bot.py "消息内容"
"""
import sys
import urllib.request
import json
import os

# Webhook 地址 - 从环境变量或配置文件读取
WEBHOOK_URL = os.environ.get('WECOM_WEBHOOK', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=530733ac-2325-499f-88f9-7bbeee786c18')

def send_text(content, mentioned_list=None, mentioned_mobile_list=None):
    """发送文本消息"""
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    if mentioned_list:
        data["text"]["mentioned_list"] = mentioned_list
    if mentioned_mobile_list:
        data["text"]["mentioned_mobile_list"] = mentioned_mobile_list
    
    return send_request(data)

def send_markdown(content):
    """发送 Markdown 消息"""
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    return send_request(data)

def send_image(base64_data, md5):
    """发送图片消息"""
    data = {
        "msgtype": "image",
        "image": {
            "base64": base64_data,
            "md5": md5
        }
    }
    return send_request(data)

def send_news(title, description, url, picurl=None):
    """发送图文消息"""
    data = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": description,
                    "url": url,
                    "picurl": picurl or ""
                }
            ]
        }
    }
    return send_request(data)

def send_request(data):
    """发送请求"""
    try:
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('errcode') == 0:
                print("✅ 消息发送成功")
                return True
            else:
                print(f"❌ 发送失败: {result.get('errmsg')}")
                return False
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 wecom_bot.py \"消息内容\"")
        print("      python3 wecom_bot.py -m \"Markdown内容\"")
        sys.exit(1)
    
    if sys.argv[1] == '-m':
        # Markdown 模式
        content = sys.argv[2] if len(sys.argv) > 2 else ""
        send_markdown(content)
    else:
        # 文本模式
        content = sys.argv[1]
        send_text(content)
