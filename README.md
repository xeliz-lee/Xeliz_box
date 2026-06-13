# Xeliz_box - Everything风格Python工具箱

MVP框架版本 - 包含基础UI框架和1个示例工具模块

## 项目结构

```
toolbox/
├── main.py                 # 程序入口
├── ui/                     # UI模块
│   ├── __init__.py
│   ├── main_window.py     # 主窗口（Everything风格）
│   ├── search_bar.py      # 搜索框
│   ├── tool_list.py       # 工具列表
│   └── status_bar.py      # 状态栏
├── tools/                  # 工具模块
│   ├── __init__.py
│   └── text_tools.py      # 文本处理工具（示例）
├── utils/                  # 工具模块
│   ├── __init__.py
│   └── config.py          # 配置管理
└── requirements.txt        # Python依赖
```

## 功能特性

### 已实现（MVP）

- ✅ **Everything风格UI**：简洁、高效、键盘驱动
- ✅ **实时搜索**：顶部搜索框，支持工具名称、描述、标签模糊匹配
- ✅ **键盘快捷键**：
  - `Ctrl+K` - 聚焦搜索框
  - `↑↓` - 选择工具
  - `Enter` - 执行工具
  - `Esc` - 隐藏到托盘
  - `Ctrl+Q` - 退出
- ✅ **系统托盘**：最小化到托盘，双击恢复
- ✅ **示例工具模块**：文本处理工具（5个工具）

### 示例工具（text_tools.py）

1. **大小写转换** - 转大写、转小写、首字母大写、切换大小写
2. **字数统计** - 统计字符数、单词数、行数、中文字数
3. **繁简互换** - 繁体转简体、简体转繁体（需安装opencc）
4. **二维码生成** - 将文本/URL生成二维码图片（需安装qrcode）
5. **密码生成** - 生成随机安全密码

## 安装依赖

```bash
# 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
```

### 依赖说明

**必需**：
- `PySide6` - Qt6 Python绑定（UI框架）

**可选**（示例工具需要）：
- `opencc-python-reimplemented` - 繁简转换
- `qrcode` - 二维码生成
- `Pillow` - 图片处理（qrcode依赖）

## 运行程序

```bash
cd toolbox
python main.py
```

## 使用说明

### 基本操作

1. **搜索工具**：在顶部搜索框输入关键词，工具列表实时过滤
   - 支持工具名称、描述、标签模糊匹配
   - 例如：输入"qrcode"或"二维码"都能找到二维码生成工具

2. **执行工具**：
   - 选中工具后按 `Enter` 键
   - 或双击工具

3. **键盘导航**：
   - `↑↓` - 在工具列表中导航
   - `Ctrl+K` - 快速聚焦搜索框
   - `Esc` - 隐藏窗口到系统托盘

4. **系统托盘**：
   - 点击右上角关闭按钮，程序会最小化到托盘
   - 双击托盘图标恢复窗口
   - 右键托盘图标可退出程序

### 添加新工具

在 `tools/` 目录下创建新的工具模块，例如 `image_tools.py`：

```python
from tools.text_tools import Tool  # 复用Tool类

class ImageTools:
    @staticmethod
    def get_tools():
        return [
            Tool(
                name="图片压缩",
                description="压缩图片大小",
                icon="🖼️",
                tags=["图片", "压缩", "image", "compress"],
                execute_func=ImageTools.compress_image
            ),
        ]
    
    @staticmethod
    def compress_image():
        # 实现图片压缩逻辑
        pass
```

然后在 `tools/__init__.py` 中注册：

```python
from tools.image_tools import ImageTools

def get_all_tools():
    all_tools = []
    all_tools.extend(TextTools.get_tools())
    all_tools.extend(ImageTools.get_tools())  # 添加这行
    return all_tools
```

## 开发路线图

### 第一阶段（MVP - 当前）
- [x] PySide6主窗口 + Everything风格UI
- [x] 搜索框（实时过滤）
- [x] 工具列表（键盘导航）
- [x] 状态栏（快捷键提示）
- [x] 系统托盘
- [x] 5个文本处理工具（示例）

### 第二阶段（核心工具）
- [ ] 图片工具（压缩、格式转换、OCR）
- [ ] PDF工具（拆分、合并、格式转换）
- [ ] 计算器合集（常规、房贷、个税）

### 第三阶段（办公效率）
- [ ] 快捷备忘（便签、待办、剪贴板历史）
- [ ] 编码辅助（时间戳、URL编解码、JSON格式化）
- [ ] 文件批量处理（重命名、清理）

### 第四阶段（优化+打包）
- [ ] 全局快捷键（Ctrl+K唤醒）
- [ ] 工具使用历史
- [ ] PyInstaller打包成exe
- [ ] 自动更新

## 技术栈

- **语言**：Python 3.8+
- **UI框架**：PySide6 (Qt6)
- **风格**：模仿Everything（简洁、高效、键盘驱动）

## 常见问题

### 1. PySide6安装失败

```bash
# 尝试使用国内镜像
pip install PySide6 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或使用 PyQt6 替代：

```bash
pip install PyQt6
# 然后将代码中的 PySide6 替换为 PyQt6
```

### 2. 繁简转换工具报错

安装 opencc-python-reimplemented：

```bash
pip install opencc-python-reimplemented
```

### 3. 二维码生成工具报错

安装 qrcode 和 Pillow：

```bash
pip install qrcode Pillow
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

---

**当前版本**：MVP 1.0  
**最后更新**：2026-05-23
