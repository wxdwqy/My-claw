"""
发送动画邮件脚本
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

CONFIG_PATH = r'C:\Users\wxd\.email\qq_config.json'
AUTH_PATH = r'C:\Users\wxd\.email\qq_auth.txt'

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def load_auth():
    with open(AUTH_PATH) as f:
        return f.read().strip()

def send_email_with_attachment(to, subject, body, attachment_path):
    config = load_config()
    password = load_auth()

    msg = MIMEMultipart()
    msg['From'] = config['email']
    msg['To'] = to
    msg['Subject'] = subject

    # 添加正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 添加附件
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        # 从路径中提取文件名
        filename = attachment_path.split('\\')[-1] if '\\' in attachment_path else attachment_path.split('/')[-1]
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)

    # 发送邮件
    with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
        server.login(config['email'], password)
        server.send_message(msg)

    print(f'已发送邮件到 {to}')
    print(f'主题: {subject}')
    print(f'附件: {attachment_path}')

if __name__ == '__main__':
    # 收件人（冬晓的QQ邮箱）
    to_email = '63224457@qq.com'

    # 邮件内容
    subject = '【云爪出品】物理动画 - 半圆形槽运动'
    body = '''你好，冬晓！

这是云爪刚才完成的物理动画训练成果！

动画展示了小球与半圆形槽的相互作用过程：
- 阶段1：球从A点正上方R处自由下落到A点
- 阶段2：球沿圆弧左半边下滑到最低点（槽不动，被墙挡住）
- 阶段3：球从底部向右上滑，槽向右运动
- 阶段4：球和槽一起向右匀速运动

物理原理：
- 机械能守恒
- 水平动量守恒（墙固定，槽可动）
- 球与槽质量相等

附件是完整的HTML动画文件，用浏览器打开即可查看和交互！

---
云爪敬上 🐾
'''

    # 附件路径
    attachment = r'C:\Users\wxd\WorkBuddy\Claw\physics_slot_animation.html'

    send_email_with_attachment(to_email, subject, body, attachment)
