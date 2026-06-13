#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xeliz_box - Everything风格的Python工具箱
"""

import sys
import os

# ============================================================
# PyInstaller 打包后需要将 _internal 目录加入 sys.path
# ============================================================
if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
    _internal_dir = os.path.join(_base_dir, '_internal')
    if os.path.isdir(_internal_dir) and _internal_dir not in sys.path:
        sys.path.insert(0, _internal_dir)
        sys.path.insert(0, _base_dir)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import Xeliz_boxWindow


def main():
    """程序入口"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Xeliz_box")
    app.setApplicationDisplayName("Xeliz_box - 工具箱")
    
    # 设置窗口图标（兼容打包和开发模式）
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # 创建主窗口
    window = Xeliz_boxWindow()
    window.show()
    
    # 运行事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
