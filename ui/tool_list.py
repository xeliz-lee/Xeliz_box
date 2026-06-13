#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具列表组件 - Everything风格
"""

from PySide6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QMessageBox
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QFont


class ToolList(QListWidget):
    """工具列表类"""
    
    # 自定义信号
    toolSelected = Signal(object)  # 工具选中信号
    toolExecuted = Signal(object)   # 工具执行信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.all_tools = []       # 所有工具
        self.filtered_tools = []  # 过滤后的工具
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化UI"""
        # 设置样式
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #F9F9F9;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #E8E8E8;
                min-height: 40px;
            }
            QListWidget::item:selected {
                background-color: #0078D7;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #E5F3FF;
            }
            QListWidget::item:selected:hover {
                background-color: #006CBF;
            }
        """)
        
        # 设置交替行颜色
        self.setAlternatingRowColors(True)
        
        # 设置图标大小（修复：使用 QSize 而不是 Qt.QSize）
        self.setIconSize(QSize(32, 32))
    
    def setup_connections(self):
        """设置信号连接"""
        # 项选中信号
        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
    
    def load_tools(self, tools):
        """加载工具列表"""
        self.all_tools = tools
        self.filtered_tools = tools  # 同步更新过滤列表
        self.refresh_list()
    
    def filter(self, keyword):
        """根据关键词过滤工具"""
        keyword = keyword.strip().lower()
        
        if not keyword:
            # 无关键词，显示所有工具
            self.filtered_tools = self.all_tools
        else:
            # 过滤工具（名称、描述、标签）
            self.filtered_tools = [
                tool for tool in self.all_tools
                if (keyword in tool.name.lower() or
                    keyword in tool.description.lower() or
                    any(keyword in tag.lower() for tag in tool.tags))
            ]
        
        self.refresh_list(self.filtered_tools)
    
    def refresh_list(self, tools=None):
        """刷新列表显示"""
        # 清空列表
        self.clear()
        
        # 使用传入的工具列表或过滤后的列表
        display_tools = tools if tools is not None else self.filtered_tools
        
        # 添加工具项
        for tool in display_tools:
            item = QListWidgetItem()
            
            # 设置显示文本
            display_text = f"{tool.icon}  {tool.name}"
            if tool.description:
                display_text += f" - {tool.description}"
            item.setText(display_text)
            
            # 设置工具提示
            if tool.tags:
                item.setToolTip(f"标签: {', '.join(tool.tags)}")
            
            # 设置字体
            font = QFont()
            font.setPointSize(11)
            item.setFont(font)
            
            # 关联工具对象
            item.setData(Qt.UserRole, tool)
            
            # 添加到列表
            self.addItem(item)
        
        # 更新过滤后的工具列表
        self.filtered_tools = display_tools
        
        # 自动选中第一项
        if self.count() > 0:
            self.setCurrentRow(0)
    
    def get_filtered_tools(self):
        """获取过滤后的工具列表"""
        return self.filtered_tools
    
    def get_selected_tool(self):
        """获取当前选中的工具"""
        current_item = self.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
    
    def on_item_clicked(self, item):
        """项点击事件"""
        tool = item.data(Qt.UserRole)
        if tool:
            self.toolSelected.emit(tool)
    
    def on_item_double_clicked(self, item):
        """项双击事件"""
        tool = item.data(Qt.UserRole)
        if tool:
            self.toolExecuted.emit(tool)
            self.execute_tool(tool)
    
    def execute_tool(self, tool):
        """执行工具"""
        try:
            tool.execute()
            if hasattr(self.parent, 'status_bar'):
                self.parent.status_bar.show_message(f"已执行: {tool.name}")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"执行失败: {str(e)}")
    
    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Enter键执行选中的工具
            tool = self.get_selected_tool()
            if tool:
                self.execute_tool(tool)
        elif event.key() == Qt.Key_Up and self.currentRow() == 0:
            # 向上箭头在第一项时，焦点回到搜索框
            if hasattr(self.parent, 'search_bar'):
                self.parent.search_bar.setFocus()
        else:
            super().keyPressEvent(event)
    
    def wheelEvent(self, event):
        """滚轮事件"""
        super().wheelEvent(event)


if __name__ == "__main__":
    # 测试代码
    pass
