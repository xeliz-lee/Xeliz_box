#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态栏组件 - 显示快捷键提示和状态信息
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class StatusBar(QWidget):
    """状态栏类"""
    
    # 自定义信号
    messageTimeout = Signal(str, int)  # 消息超时信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化UI"""
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        # 快捷键提示标签
        self.shortcut_label = QLabel()
        self.shortcut_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.shortcut_label)
        
        # 状态信息标签
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.addWidget(self.status_label)
        
        # 右侧信息标签（工具数量等）
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.info_label)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                border-top: 1px solid #CCCCCC;
            }
            QLabel {
                color: #666666;
                font-size: 11px;
                padding: 2px 5px;
            }
        """)
        
        # 设置字体
        font = QFont()
        font.setPointSize(9)
        self.shortcut_label.setFont(font)
        self.status_label.setFont(font)
        self.info_label.setFont(font)
        
        # 初始化显示
        self.update_shortcuts()
    
    def setup_connections(self):
        """设置信号连接"""
        # 连接消息超时信号
        self.messageTimeout.connect(self.show_temporary_message)
    
    def update_shortcuts(self):
        """更新快捷键显示"""
        shortcuts = [
            "Ctrl+K 搜索",
            "↑↓ 选择",
            "Enter 执行",
            "Esc 隐藏"
        ]
        self.shortcut_label.setText(" | ".join(shortcuts))
    
    def update_info(self, total_tools=0, filtered_tools=0):
        """更新工具数量信息"""
        if filtered_tools == total_tools:
            self.info_label.setText(f"共 {total_tools} 个工具")
        else:
            self.info_label.setText(f"显示 {filtered_tools}/{total_tools} 个工具")
    
    def show_message(self, message, timeout=3000):
        """显示状态消息"""
        self.status_label.setText(message)
        
        # 定时恢复
        if timeout > 0:
            self.messageTimeout.emit(message, timeout)
    
    def show_temporary_message(self, message, timeout):
        """显示临时消息"""
        # 保存原消息
        original = self.status_label.text()
        
        # 显示新消息
        self.status_label.setText(message)
        
        # 定时恢复（简化版，实际应该用QTimer）
        # 这里暂时不实现定时器，由调用者负责恢复
    
    def clear_message(self):
        """清除状态消息"""
        self.status_label.clear()
    
    def set_tool_count(self, count):
        """设置工具数量"""
        self.info_label.setText(f"共 {count} 个工具")
    
    def update_status(self, text):
        """更新状态文本"""
        self.status_label.setText(text)
    
    def clear_status(self):
        """清除状态"""
        self.status_label.clear()
        self.update_shortcuts()
