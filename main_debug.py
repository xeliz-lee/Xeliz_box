#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xeliz_box Debug Version - 显示详细错误信息"""

import sys
import os
import traceback

# PyInstaller path fix
if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
    _internal_dir = os.path.join(_base_dir, '_internal')
    if os.path.isdir(_internal_dir):
        sys.path.insert(0, _internal_dir)
        sys.path.insert(0, _base_dir)

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Xeliz_box [DEBUG]")
    
    # 收集所有调试信息
    debug_info = []
    debug_info.append(f"sys.executable: {sys.executable}")
    debug_info.append(f"sys.path[0]: {sys.path[0]}")
    debug_info.append(f"frozen: {getattr(sys, 'frozen', False)}")
    debug_info.append(f"")
    
    # 测试1: import tools.base
    try:
        from tools.base import Tool
        debug_info.append(f"✅ from tools.base import Tool -> OK")
    except Exception as e:
        debug_info.append(f"❌ from tools.base import Tool FAILED: {e}")
        debug_info.append(traceback.format_exc())
    
    # 测试2: import tools
    try:
        import tools
        debug_info.append(f"✅ import tools -> OK ({tools.__file__})")
    except Exception as e:
        debug_info.append(f"❌ import tools FAILED: {e}")
        debug_info.append(traceback.format_exc())
    
    # 测试3: get_all_tools()
    try:
        from tools import get_all_tools
        all_tools = get_all_tools()
        debug_info.append(f"✅ get_all_tools() -> {len(all_tools)} tools")
    except Exception as e:
        debug_info.append(f"❌ get_all_tools() FAILED: {e}")
        debug_info.append(traceback.format_exc())
    
    # 弹窗显示
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Debug Info")
    msg.setText("\n".join(debug_info))
    msg.setDetailedText(f"Full sys.path:\n" + "\n".join(sys.path))
    msg.exec_()
    
    # 正常启动窗口
    from ui.main_window import Xeliz_boxWindow
    window = Xeliz_boxWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
