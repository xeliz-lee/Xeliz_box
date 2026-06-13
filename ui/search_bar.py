#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索框组件 - Everything风格
"""

from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal, Qt


class SearchBar(QLineEdit):
    """搜索框类"""
    
    # 自定义信号
    textChanged = Signal(str)  # 文本变化信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化UI"""
        # 设置占位符文本
        self.setPlaceholderText("搜索工具... (Ctrl+K)")
        
        # 设置工具提示
        self.setToolTip("输入关键词搜索工具，支持模糊匹配")
        
        # 设置清除按钮
        self.setClearButtonEnabled(True)
        
        # 设置样式
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                font-size: 14px;
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #0078D7;
            }
            QToolButton {
                background-color: transparent;
                border: none;
            }
        """)
    
    def setup_connections(self):
        """设置信号连接"""
        # 文本变化信号
        self.textChanged.connect(self.on_text_changed)
    
    def on_text_changed(self, text):
        """文本变化处理"""
        # 过滤工具列表
        if hasattr(self.parent, 'tool_list'):
            self.parent.tool_list.filter(text)
        
        # 发送自定义信号
        self.textChanged.emit(text)
    
    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key_Down:
            # 向下箭头，焦点移到工具列表
            if hasattr(self.parent, 'tool_list'):
                self.parent.tool_list.setFocus()
                self.parent.tool_list.setCurrentRow(0)
        elif event.key() == Qt.Key_Escape:
            # Esc键，清除搜索框
            self.clear()
        else:
            super().keyPressEvent(event)
    
    def focusInEvent(self, event):
        """获得焦点事件"""
        super().focusInEvent(event)
        # 全选文本
        self.selectAll()
    
    def get_keywords(self):
        """获取搜索关键词"""
        return self.text().strip()
    
    def clear_search(self):
        """清除搜索"""
        self.clear()
        self.setFocus()
