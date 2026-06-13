#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具基类模块
所有工具模块共享的 Tool 类定义
"""

from typing import Callable, List


class Tool:
    """
    工具类 - 统一的工具数据结构
    
    所有工具模块都使用这个类来创建工具实例。
    """
    
    def __init__(self, name: str, description: str, icon: str, 
                 tags: List[str], execute_func: Callable):
        """
        初始化工具
        
        Args:
            name: 工具名称
            description: 工具描述（一行话）
            icon: 图标（emoji 字符串）
            tags: 标签列表（用于搜索过滤）
            execute_func: 执行函数（无参数，调用时执行工具逻辑）
        """
        self.name = name
        self.description = description
        self.icon = icon
        self.tags = tags
        self.execute_func = execute_func
    
    def execute(self):
        """执行工具"""
        if self.execute_func:
            return self.execute_func()
    
    def __repr__(self):
        return f"Tool({self.name})"
    
    def to_dict(self):
        """转换为字典（用于序列化）"""
        return {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "tags": self.tags,
        }
