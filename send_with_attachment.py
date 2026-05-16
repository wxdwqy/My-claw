"""
发送带附件的邮件
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

CONFIG_PATH = r'C:\Users\wxd\.email\qq_config.json'
AUTH_PATH = r'C:\Users\wxd\.email\qq_auth.txt'

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def load_auth():
    with open(AUTH_PATH) as f:
        return f.read().strip()

def send_email_with_attachments(to, subject, body, attachments):
    """
    发送带附件的邮件
    attachments: 文件路径列表
    """
    config = load_config()
    password = load_auth()
    
    msg = MIMEMultipart()
    msg['From'] = config['email']
    msg['To'] = to
    msg['Subject'] = subject
    
    # 正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 附件
    for filepath in attachments:
        if not os.path.exists(filepath):
            print(f'文件不存在: {filepath}')
            continue
        
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        filename = os.path.basename(filepath)
        # 处理中文文件名
        try:
            from email.header import Header
            filename_encoded = Header(filename, 'utf-8').encode()
        except:
            filename_encoded = filename
        
        part.add_header('Content-Disposition', 'attachment', filename=filename_encoded)
        encoders.encode_base64(part)
        msg.attach(part)
        print(f'已添加附件: {filename}')
    
    # 发送
    with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
        server.login(config['email'], password)
        server.send_message(msg)
    
    print(f'\n✅ 邮件已发送到: {to}')
    print(f'主题: {subject}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', required=True)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--body', default='')
    parser.add_argument('--attach', nargs='*', default=[])
    args = parser.parse_args()
    
    send_email_with_attachments(args.to, args.subject, args.body, args.attach)
