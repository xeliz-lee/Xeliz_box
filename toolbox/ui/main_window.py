#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口 - Everything风格
"""

import sys
import os
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, 
                               QSystemTrayIcon, QMenu, QMessageBox)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QAction, QKeySequence, QShortcut
from ui.search_bar import SearchBar
from ui.tool_list import ToolList
from ui.status_bar import StatusBar


class Xeliz_boxWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.tools = []  # 工具列表
        self.init_ui()
        self.load_tools()
        self.setup_shortcuts()
        self.setup_tray()
    
    def init_ui(self):
        """初始化UI"""
        # 窗口设置（与 app.setApplicationDisplayName 保持一致，避免 Windows 标题重复）
        self.setWindowTitle("Xeliz_box - 工具箱")
        self.setMinimumSize(600, 400)
        self.resize(800, 600)
        
        # 窗口样式（Everything风格：简洁、无边框感）
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #0078D7;
            }
            QListWidget {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
            QListWidget::item:selected {
                background-color: #0078D7;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #E5F3FF;
            }
            QLabel {
                padding: 4px;
                color: #666666;
                font-size: 12px;
            }
        """)
        
        # 中央Widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # 布局
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 搜索框
        self.search_bar = SearchBar(self)
        layout.addWidget(self.search_bar)
        
        # 工具列表
        self.tool_list = ToolList(self)
        layout.addWidget(self.tool_list)
        
        # 状态栏
        self.status_bar = StatusBar(self)
        layout.addWidget(self.status_bar)
        
        # 设置焦点
        self.search_bar.setFocus()
    
    def load_tools(self):
        """加载所有工具"""
        try:
            from tools import get_all_tools
            self.tools = get_all_tools()
        except Exception as e:
            print(f"Warning: Could not load all tools: {e}")
            # Fallback: only load text tools
            from tools.text_tools import TextTools
            self.tools = TextTools.get_tools()
        
        # 将工具传递给 ToolList 组件（关键修复！）
        self.tool_list.load_tools(self.tools)
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # Ctrl+Q 退出（真正退出进程）
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.force_quit)
        
        # Esc 隐藏到托盘
        esc_shortcut = QShortcut(QKeySequence("Esc"), self)
        esc_shortcut.activated.connect(self.hide_to_tray)
        
        # Ctrl+K 聚焦搜索框
        search_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        search_shortcut.activated.connect(self.focus_search)
    
    def setup_tray(self):
        """设置系统托盘"""
        # 查找 icon.ico（支持打包后路径）
        if getattr(sys, 'frozen', False):
            _base_dir = os.path.dirname(sys.executable)
        else:
            # 开发模式：从 ui/ 目录回退到 toolbox/ 根目录
            _base_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.basename(_base_dir) == 'ui':
                _base_dir = os.path.dirname(_base_dir)
        
        icon_path = os.path.join(_base_dir, "icon.ico")
        if os.path.exists(icon_path):
            tray_icon_obj = QIcon(icon_path)
        else:
            tray_icon_obj = QIcon()
            # 打印警告以便定位问题（只在开发模式）
            if not getattr(sys, 'frozen', False):
                print(f"[Xeliz_box] icon.ico not found at: {icon_path}", flush=True)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(tray_icon_obj)
        
        # 托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show_normal)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.force_quit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 点击托盘图标显示窗口
        self.tray_icon.activated.connect(self.tray_activated)
    
    def show_normal(self):
        """正常显示窗口（取消最小化/激活）"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def focus_search(self):
        """聚焦搜索框"""
        self.search_bar.selectAll()
        self.search_bar.setFocus()
    
    def hide_to_tray(self):
        """隐藏到托盘"""
        self.hide()
        # 只有当托盘图标有效时才显示通知
        if self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                "Xeliz_box",
                "已最小化到系统托盘，右键菜单可退出",
                QSystemTrayIcon.Information,
                2000
            )
    
    def tray_activated(self, reason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal()
    
    def force_quit(self):
        """强制退出（彻底关闭程序）"""
        self.tray_icon.hide()
        self.close()
        # 强制退出：QApplication 不走事件循环
        import sys as _sys
        _sys.exit(0)
    
    def execute_selected_tool(self):
        """执行选中的工具"""
        current_row = self.tool_list.currentRow()
        filtered = self.tool_list.get_filtered_tools()
        if current_row >= 0 and current_row < len(filtered):
            tool = filtered[current_row]
            try:
                tool.execute()
                self.status_bar.show_message(f"已执行: {tool.name}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"执行失败: {str(e)}")
    
    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Enter键执行选中的工具
            self.execute_selected_tool()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """关闭事件：点 X 隐藏到托盘（不退出进程）"""
        event.ignore()
        self.hide_to_tray()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Xeliz_box - 工具箱")
    window = Xeliz_boxWindow()
    window.show()
    sys.exit(app.exec())
