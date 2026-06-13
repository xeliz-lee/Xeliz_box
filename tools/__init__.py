#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块初始化
包含所有工具的定义和注册
"""

from tools.text_tools import TextTools
from tools.image_tools import ImageTools
from tools.calculator_tools import CalculatorTools
from tools.office_tools import OfficeTools
from tools.fun_tools import FunTools


def get_all_tools():
    """获取所有工具"""
    all_tools = []
    
    # 文本处理工具
    all_tools.extend(TextTools.get_tools())
    
    # 图片工具
    all_tools.extend(ImageTools.get_tools())
    
    # 计算器工具
    all_tools.extend(CalculatorTools.get_tools())
    
    # 办公效率工具
    all_tools.extend(OfficeTools.get_tools())
    
    # 趣味娱乐工具
    all_tools.extend(FunTools.get_tools())
    
    return all_tools


__all__ = ['get_all_tools', 'TextTools', 'ImageTools', 'CalculatorTools', 'OfficeTools', 'FunTools']
