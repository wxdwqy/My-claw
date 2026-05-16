# PS 2020 自动化技能 (PS-Automation-2020)

## 简介
通过 Python + COM + DoJavaScript 操控 Photoshop 2020，实现局部修图自动化。

## 环境要求
- PS 2020 (21.0.0)+ 已安装
- Python 3.11 + win32com

## 核心发现

### PS 2020 vs CC 2019 关键差异

| 功能 | CC 2019 | PS 2020 |
|------|---------|---------|
| activeDocument | ❌ | ✅ |
| doc.paste() | ❌ | ✅ |
| selection.fill() | ❌ | ✅ |
| 加载通道为选区 | ❌ | ✅ |
| executeMenuCommand | ❌ | ❌ |

**结论：PS 2020 的 COM 接口比 CC 2019 完整很多，必须升级到 2020！**

## 连接方式

```python
import win32com.client
import pythoncom

pythoncom.CoInitializeEx(0)
psApp = win32com.client.Dispatch('Photoshop.Application')
doc = psApp.Application.Documents.Item(1)
# ... 操作 ...
pythoncom.CoUninitialize()
```

## 已验证可用的操作

### 1. 基本连接
```python
psApp = win32com.client.Dispatch('Photoshop.Application')
docs = psApp.Application.Documents
doc = docs.Item(1)  # 当前文档
```

### 2. DoJavaScript 执行
```python
js = '''
var doc = app.activeDocument;
doc.selection.selectAll();
doc.selection.copy();
'''
psApp.DoJavaScript(js)
```

### 3. 创建 Alpha 通道
```javascript
var alphaChan = doc.channels.add();
alphaChan.name = 'Mask_Name';
doc.activeChannels = [alphaChan];
```

### 4. 打开外部文件
```javascript
var maskFile = new File('C:/path/to/mask.png');
var maskDoc = app.open(maskFile);
```

### 5. 复制/粘贴
```javascript
maskDoc.selection.selectAll();
maskDoc.selection.copy();
maskDoc.close(SaveOptions.DONOTSAVECHANGES);
app.activeDocument = doc;
doc.paste();
```

### 6. 加载通道为选区
```javascript
var desc = new ActionDescriptor();
var ref1 = new ActionReference();
ref1.putProperty(stringIDToTypeID('channel'), stringIDToTypeID('selection'));
desc.putReference(charIDToTypeID('null'), ref1);
var ref2 = new ActionReference();
ref2.putName(stringIDToTypeID('channel'), 'ChannelName');
desc.putReference(stringIDToTypeID('to'), ref2);
executeAction(stringIDToTypeID('set'), desc, DialogModes.NO);
```

### 7. 填充选区
```javascript
doc.selection.fill(app.foregroundColor);
```

## 完整工作流

### SAM 蒙版 → PS 选区 → 填充
```python
js = '''
var doc = app.activeDocument;

// 1. 打开蒙版
var maskFile = new File('C:/path/to/mask.png');
var maskDoc = app.open(maskFile);

// 2. 复制蒙版
maskDoc.selection.selectAll();
maskDoc.selection.copy();
maskDoc.close(SaveOptions.DONOTSAVECHANGES);

// 3. 回到原图
app.activeDocument = doc;

// 4. 创建 Alpha 通道
var alphaChan = doc.channels.add();
alphaChan.name = 'SAM_Mask';
doc.activeChannels = [alphaChan];

// 5. 粘贴蒙版
doc.paste();

// 6. 载入选区
doc.activeChannels = [alphaChan];
var desc = new ActionDescriptor();
var ref1 = new ActionReference();
ref1.putProperty(stringIDToTypeID('channel'), stringIDToTypeID('selection'));
desc.putReference(charIDToTypeID('null'), ref1);
var ref2 = new ActionReference();
ref2.putName(stringIDToTypeID('channel'), 'SAM_Mask');
desc.putReference(stringIDToTypeID('to'), ref2);
executeAction(stringIDToTypeID('set'), desc, DialogModes.NO);

// 7. 切换回 RGB
doc.activeChannels = [doc.channels[0], doc.channels[1], doc.channels[2]];

// 8. 填充
doc.selection.fill(app.foregroundColor);
'''
psApp.DoJavaScript(js)
```

### 保存文件
```javascript
var doc = app.activeDocument;
var saveFile = new File('C:/path/to/output.png');
var saveOptions = new PNGSaveOptions();
saveOptions.compression = 9;
doc.saveAs(saveFile, saveOptions);
```

### 填充选区
```javascript
doc.selection.fill(app.foregroundColor);
```

## 已知限制

### 内容感知填充
- PS 2020 的内容感知填充（Content-Aware Fill）没有直接的 JS API
- `executeAction('CntS')` ❌ 不可用
- `executeMenuCommand('fill')` ❌ 不可用
- **替代方案**：先用 SAM + LaMa 修复，再用 PS 粘贴/合成

### 图层类型
- `LayerKind.SOLIDFILL` 在 PS 2020 不可用
- 只能创建普通图层或文字图层

## 已验证（2026-04-18）

| 功能 | 状态 | 备注 |
|------|------|------|
| COM 连接 | ✅ | |
| DoJavaScript | ✅ | |
| activeDocument 切换 | ✅ | |
| 创建 Alpha 通道 | ✅ | |
| 打开外部文件 | ✅ | |
| 复制/粘贴 | ✅ | doc.paste() |
| 加载通道为选区 | ✅ | ActionDescriptor |
| selection.fill() | ✅ | |
| 保存 PNG | ✅ | |
| 亮度/对比度 | ⚠️ | 需要全画布选区 |
| 创建新图层 | ✅ | |

## 注意事项

1. **必须用 PS 2020**，CC 2019 接口不完整
2. **COM 连接后要 CoUninitialize()**
3. **蒙版必须是灰度图**（模式 L）
4. **先验证蒙版有效**：检查白色像素 > 0
5. **选区操作用 ActionDescriptor 方式**比直接 DOM 更可靠
