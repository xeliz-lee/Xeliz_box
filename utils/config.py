#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

from PySide6.QtCore import QSettings


class Config:
    """配置管理类"""
    
    # 配置键常量
    KEY_WINDOW_GEOMETRY = "window/geometry"
    KEY_WINDOW_STATE = "window/state"
    KEY_RECENT_TOOLS = "tools/recent"
    KEY_MAX_RECENT = "tools/max_recent"
    KEY_STARTUP_MINIMIZED = "startup/minimized"
    KEY_GLOBAL_HOTKEY = "hotkey/global"
    
    def __init__(self):
        """初始化配置"""
        self.settings = QSettings("Xeliz_box", "Xeliz_box")
    
    def get(self, key: str, default=None):
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self.settings.value(key, default)
    
    def set(self, key: str, value):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.settings.setValue(key, value)
    
    def remove(self, key: str):
        """
        删除配置
        
        Args:
            key: 配置键
        """
        self.settings.remove(key)
    
    def contains(self, key: str) -> bool:
        """
        检查配置是否存在
        
        Args:
            key: 配置键
            
        Returns:
            bool: 是否存在
        """
        return self.settings.contains(key)
    
    def clear(self):
        """清除所有配置"""
        self.settings.clear()
    
    def sync(self):
        """同步配置到磁盘"""
        self.settings.sync()
    
    def get_recent_tools(self, max_count: int = None) -> list:
        """
        获取最近使用的工具
        
        Args:
            max_count: 最大数量，None表示使用配置的值
            
        Returns:
            list: 工具名称列表
        """
        if max_count is None:
            max_count = self.get(self.KEY_MAX_RECENT, 10)
        
        recent = self.get(self.KEY_RECENT_TOOLS, [])
        if isinstance(recent, str):
            recent = [recent]
        
        return recent[:max_count]
    
    def add_recent_tool(self, tool_name: str):
        """
        添加最近使用的工具
        
        Args:
            tool_name: 工具名称
        """
        recent = self.get_recent_tools()
        
        # 移除已存在的
        if tool_name in recent:
            recent.remove(tool_name)
        
        # 添加到开头
        recent.insert(0, tool_name)
        
        # 限制数量
        max_count = self.get(self.KEY_MAX_RECENT, 10)
        recent = recent[:max_count]
        
        # 保存
        self.set(self.KEY_RECENT_TOOLS, recent)
        self.sync()
    
    def get_window_geometry(self):
        """获取窗口位置和大小"""
        return self.get(self.KEY_WINDOW_GEOMETRY)
    
    def set_window_geometry(self, geometry):
        """保存窗口位置和大小"""
        self.set(self.KEY_WINDOW_GEOMETRY, geometry)
        self.sync()
    
    def get_window_state(self):
        """获取窗口状态"""
        return self.get(self.KEY_WINDOW_STATE)
    
    def set_window_state(self, state):
        """保存窗口状态"""
        self.set(self.KEY_WINDOW_STATE, state)
        self.sync()
    
    def is_startup_minimized(self) -> bool:
        """是否启动时最小化"""
        return self.get(self.KEY_STARTUP_MINIMIZED, False)
    
    def set_startup_minimized(self, minimized: bool):
        """设置是否启动时最小化"""
        self.set(self.KEY_STARTUP_MINIMIZED, minimized)
        self.sync()
    
    def get_global_hotkey(self) -> str:
        """获取全局快捷键"""
        return self.get(self.KEY_GLOBAL_HOTKEY, "Ctrl+Alt+T")
    
    def set_global_hotkey(self, hotkey: str):
        """设置全局快捷键"""
        self.set(self.KEY_GLOBAL_HOTKEY, hotkey)
        self.sync()
    
    @staticmethod
    def instance():
        """获取单例实例"""
        if not hasattr(Config, '_instance'):
            Config._instance = Config()
        return Config._instance


# 全局配置实例
config = Config.instance()

__all__ = ['Config', 'config']
