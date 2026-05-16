import zipfile
import xml.etree.ElementTree as ET

# 读取 docx 文件
doc = zipfile.ZipFile('C:/Users/wxd/WorkBuddy/Claw/b.docx')
xml_content = doc.read('word/document.xml')

# 解析 XML
root = ET.fromstring(xml_content)

# 提取所有文本
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
texts = []
for t in root.findall('.//w:t', ns):
    if t.text:
        texts.append(t.text)

# 写入文件（UTF-8 编码）
with open('C:/Users/wxd/WorkBuddy/Claw/b_answer.txt', 'w', encoding='utf-8') as f:
    f.write(''.join(texts))

print('提取完成！')
