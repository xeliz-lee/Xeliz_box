#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趣味娱乐工具模块 - 完整实现
"""

import random
import datetime
import json
import os
from tools.base import Tool
from typing import Callable, List
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLineEdit, QTextEdit, QPushButton, QLabel,
                               QComboBox, QSpinBox, QMessageBox, QFileDialog,
                               QInputDialog, QProgressDialog, QColorDialog)
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtCore import Qt, QRect
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO


class FunTools:
    """趣味娱乐工具集"""
    
    @staticmethod
    def get_tools() -> List:
        """
        获取所有趣味娱乐工具
        
        Returns:
            List: 工具列表
        """
        return [
            # 随机工具
            Tool(
                name="抽签摇号",
                description="随机抽签或摇号",
                icon="🎲",
                tags=["抽签", "摇号", "随机", "lottery", "random"],
                execute_func=FunTools.lottery
            ),
            Tool(
                name="随机点名",
                description="从名单中随机点名",
                icon="👥",
                tags=["点名", "随机", "名单", "name", "picker"],
                execute_func=FunTools.name_picker
            ),
            Tool(
                name="骰子转盘",
                description="掷骰子或转盘随机选择",
                icon="🎰",
                tags=["骰子", "转盘", "随机", "dice", "wheel", "roulette"],
                execute_func=FunTools.dice_wheel
            ),
            Tool(
                name="性格趣味测算",
                description="趣味性格测试（娱乐向）",
                icon="🧠",
                tags=["性格", "测试", "趣味", "personality", "test", "fun"],
                execute_func=FunTools.personality_test
            ),
            
            # 创意工具
            Tool(
                name="表情包制作",
                description="制作自定义表情包",
                icon="😂",
                tags=["表情包", "制作", "meme", "sticker"],
                execute_func=FunTools.meme_generator
            ),
            Tool(
                name="头像简易美化",
                description="简易美化头像（滤镜、边框等）",
                icon="📸",
                tags=["头像", "美化", "滤镜", "avatar", "beautify", "filter"],
                execute_func=FunTools.avatar_beautifier
            ),
            Tool(
                name="配色取色器",
                description="从图片提取配色方案或使用取色器",
                icon="🎨",
                tags=["配色", "取色", "颜色", "color", "palette", "picker"],
                execute_func=FunTools.color_picker
            ),
            
            # 文本生成工具
            Tool(
                name="短句文案生成",
                description="生成朋友圈文案、签名等短句",
                icon="✍️",
                tags=["文案", "生成", "短句", "签名", "copywriting", "text"],
                execute_func=FunTools.text_generator
            ),
            Tool(
                name="网名昵称设计",
                description="生成个性化的网名或昵称",
                icon="👤",
                tags=["网名", "昵称", "生成", "username", "nickname", "generator"],
                execute_func=FunTools.nickname_generator
            ),
        ]
    
    # ==================== 随机工具 ====================
    
    @staticmethod
    def lottery():
        """抽签摇号"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("抽签摇号")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # 输入选项（用逗号分隔）
        form = QFormLayout()
        
        options_input = QTextEdit()
        options_input.setPlaceholderText("请输入选项，每行一个或逗号分隔")
        options_input.setMaximumHeight(100)
        form.addRow("选项:", options_input)
        
        # 抽签次数
        times_spin = QSpinBox()
        times_spin.setRange(1, 10)
        times_spin.setValue(1)
        form.addRow("抽签次数:", times_spin)
        
        layout.addLayout(form)
        
        # 结果显示
        result_label = QLabel("结果将显示在这里")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px;")
        layout.addWidget(result_label)
        
        # 抽签按钮
        lottery_btn = QPushButton("开始抽签")
        lottery_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        lottery_btn.clicked.connect(lambda: FunTools._do_lottery(
            options_input.toPlainText(),
            times_spin.value(),
            result_label
        ))
        layout.addWidget(lottery_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _do_lottery(options_text, times, result_label):
        """执行抽签"""
        # 解析选项
        options = []
        for line in options_text.split('\n'):
            line = line.strip()
            if line:
                # 支持逗号分隔
                options.extend([opt.strip() for opt in line.split(',') if opt.strip()])
        
        if not options:
            result_label.setText("请输入选项！")
            result_label.setStyleSheet("color: red;")
            return
        
        # 抽签
        results = random.choices(options, k=times)
        
        if times == 1:
            result_text = f"🎉 抽签结果：\n\n{results[0]}"
        else:
            result_text = "🎉 抽签结果：\n\n" + "\n".join([f"{i+1}. {r}" for i, r in enumerate(results)])
        
        result_label.setText(result_text)
        result_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px; color: #2196F3;")
    
    @staticmethod
    def name_picker():
        """随机点名"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("随机点名")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 输入名单
        layout.addWidget(QLabel("请输入名单（每行一个名字）:"))
        
        name_input = QTextEdit()
        name_input.setPlaceholderText("张三\n李四\n王五\n...")
        layout.addWidget(name_input)
        
        # 已点名列表
        picked_label = QLabel("已点名:")
        layout.addWidget(picked_label)
        
        picked_list = QTextEdit()
        picked_list.setReadOnly(True)
        picked_list.setMaximumHeight(100)
        layout.addWidget(picked_list)
        
        # 点名按钮
        pick_btn = QPushButton("开始点名")
        pick_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        
        remaining_names = []
        
        def start_picking():
            nonlocal remaining_names
            
            # 获取名单
            names_text = name_input.toPlainText()
            all_names = [n.strip() for n in names_text.split('\n') if n.strip()]
            
            if not all_names:
                QMessageBox.warning(None, "警告", "请输入名单！")
                return
            
            # 初始化剩余名单
            if not remaining_names:
                remaining_names = all_names.copy()
            
            if not remaining_names:
                QMessageBox.information(None, "完成", "所有人都已被点名！")
                return
            
            # 随机选择一个
            picked = random.choice(remaining_names)
            remaining_names.remove(picked)
            
            # 显示结果
            current_picked = picked_list.toPlainText()
            picked_list.setText(current_picked + f"{picked}\n")
            
            # 弹窗提示
            QMessageBox.information(None, "点名结果", f"🎯 点到: {picked}")
        
        pick_btn.clicked.connect(start_picking)
        layout.addWidget(pick_btn)
        
        # 重置按钮
        def reset():
            nonlocal remaining_names
            remaining_names = []
            picked_list.clear()
        
        reset_btn = QPushButton("重置")
        reset_btn.clicked.connect(reset)
        layout.addWidget(reset_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def dice_wheel():
        """骰子转盘"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("骰子转盘")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # 模式选择
        mode_combo = QComboBox()
        mode_combo.addItems(["骰子（1-6）", "自定义转盘"])
        layout.addWidget(QLabel("选择模式:"))
        layout.addWidget(mode_combo)
        
        # 自定义选项（默认隐藏）
        custom_input = QTextEdit()
        custom_input.setPlaceholderText("输入转盘选项，每行一个")
        custom_input.setVisible(False)
        layout.addWidget(custom_input)
        
        def toggle_custom_input(index):
            custom_input.setVisible(index == 1)
        
        mode_combo.currentIndexChanged.connect(toggle_custom_input)
        
        # 结果显示
        result_label = QLabel("?")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-size: 48px; font-weight: bold; padding: 20px;")
        layout.addWidget(result_label)
        
        # 掷骰子/转盘按钮
        roll_btn = QPushButton("掷骰子")
        roll_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        
        def roll():
            mode = mode_combo.currentIndex()
            
            if mode == 0:  # 骰子
                result = random.randint(1, 6)
                result_label.setText(str(result))
                result_label.setStyleSheet("font-size: 48px; font-weight: bold; padding: 20px; color: #4CAF50;")
            else:  # 转盘
                options_text = custom_input.toPlainText()
                options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
                
                if not options:
                    QMessageBox.warning(None, "警告", "请输入转盘选项！")
                    return
                
                result = random.choice(options)
                result_label.setText(result)
                result_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px; color: #2196F3;")
        
        roll_btn.clicked.connect(roll)
        layout.addWidget(roll_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def personality_test():
        """性格趣味测算（娱乐向）"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("性格趣味测算")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 问题列表
        questions = [
            "你更喜欢独处还是社交？",
            "你做决定时更依赖逻辑还是直觉？",
            "你更喜欢计划还是随性？",
            "你更注重细节还是整体？",
            "你更喜欢文字还是图像？"
        ]
        
        answers = []
        
        for q in questions:
            layout.addWidget(QLabel(q))
            
            combo = QComboBox()
            combo.addItems(["A. 偏向前者", "B. 偏向后者", "C. 不确定"])
            layout.addWidget(combo)
            
            answers.append(combo)
        
        # 测算按钮
        def calculate():
            # 统计答案
            a_count = sum(1 for ans in answers if ans.currentText().startswith('A'))
            b_count = sum(1 for ans in answers if ans.currentText().startswith('B'))
            
            # 生成趣味结果（纯娱乐）
            if a_count > b_count:
                result = """🧠 性格分析结果（趣味版）

你是一个偏内向、理性的人。

特点：
- 喜欢深度思考
- 做事有条理
- 重视个人空间
- 对细节敏感

适合的职业：程序员、作家、设计师

（本测试纯属娱乐，请勿当真😄）"""
            elif b_count > a_count:
                result = """🧠 性格分析结果（趣味版）

你是一个偏外向、感性的人。

特点：
- 喜欢社交活动
- 直觉敏锐
- 行动力强
- 重视人际关系

适合的职业：销售、教师、公关

（本测试纯属娱乐，请勿当真😄）"""
            else:
                result = """🧠 性格分析结果（趣味版）

你是一个平衡型人格。

特点：
- 内外兼修
- 理性与感性并存
- 适应能力强
- 善于协调

适合的职业：项目经理、HR、咨询顾问

（本测试纯属娱乐，请勿当真😄）"""
            
            QMessageBox.information(None, "测算结果", result)
        
        calc_btn = QPushButton("开始测算")
        calc_btn.clicked.connect(calculate)
        layout.addWidget(calc_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    # ==================== 创意工具 ====================
    
    @staticmethod
    def meme_generator():
        """表情包制作"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("表情包制作")
        dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # 选择底图
        layout.addWidget(QLabel("选择表情包底图:"))
        
        image_label = QLabel("未选择图片")
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        layout.addWidget(image_label)
        
        image_path = None
        
        def select_image():
            nonlocal image_path
            file_path, _ = QFileDialog.getOpenFileName(
                None,
                "选择图片",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
            )
            
            if file_path:
                image_path = file_path
                pixmap = QPixmap(file_path)
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        
        select_btn = QPushButton("选择图片")
        select_btn.clicked.connect(select_image)
        layout.addWidget(select_btn)
        
        # 输入文字
        layout.addWidget(QLabel("输入文字（支持多行）:"))
        
        text_input = QTextEdit()
        text_input.setPlaceholderText("输入表情包文字...")
        text_input.setMaximumHeight(100)
        layout.addWidget(text_input)
        
        # 文字位置
        position_combo = QComboBox()
        position_combo.addItems(["顶部", "底部", "中间"])
        layout.addWidget(QLabel("文字位置:"))
        layout.addWidget(position_combo)
        
        # 生成按钮
        def generate():
            if not image_path:
                QMessageBox.warning(None, "警告", "请先选择图片！")
                return
            
            if not text_input.toPlainText():
                QMessageBox.warning(None, "警告", "请输入文字！")
                return
            
            try:
                # 打开图片
                img = Image.open(image_path)
                
                # 创建绘图对象
                draw = ImageDraw.Draw(img)
                
                # 尝试加载字体
                try:
                    font = ImageFont.truetype("msyh.ttc", 40)
                except:
                    font = ImageFont.load_default()
                
                # 文字位置
                text = text_input.toPlainText()
                position = position_combo.currentText()
                
                # 获取文字大小
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # 计算位置
                if position == "顶部":
                    pos = ((img.width - text_width) // 2, 10)
                elif position == "底部":
                    pos = ((img.width - text_width) // 2, img.height - text_height - 10)
                else:  # 中间
                    pos = ((img.width - text_width) // 2, (img.height - text_height) // 2)
                
                # 绘制文字（带描边效果）
                # 先画黑色描边
                for offset in [(x, y) for x in [-2, 0, 2] for y in [-2, 0, 2] if not (x == 0 and y == 0)]:
                    draw.text((pos[0] + offset[0], pos[1] + offset[1]), text, font=font, fill=(0, 0, 0))
                
                # 再画白色文字
                draw.text(pos, text, font=font, fill=(255, 255, 255))
                
                # 保存
                output_path, _ = QFileDialog.getSaveFileName(
                    None,
                    "保存表情包",
                    "meme.png",
                    "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
                )
                
                if output_path:
                    img.save(output_path)
                    QMessageBox.information(None, "成功", f"表情包已保存到:\n{output_path}")
                    
                    # 显示生成的图片
                    pixmap = QPixmap(output_path)
                    image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        
            except Exception as e:
                QMessageBox.warning(None, "错误", f"生成失败: {str(e)}")
        
        generate_btn = QPushButton("生成表情包")
        generate_btn.clicked.connect(generate)
        layout.addWidget(generate_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def avatar_beautifier():
        """头像简易美化"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("头像简易美化")
        dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # 选择头像
        layout.addWidget(QLabel("选择头像图片:"))
        
        image_label = QLabel("未选择图片")
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        layout.addWidget(image_label)
        
        image_path = None
        
        def select_image():
            nonlocal image_path
            file_path, _ = QFileDialog.getOpenFileName(
                None,
                "选择图片",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
            )
            
            if file_path:
                image_path = file_path
                pixmap = QPixmap(file_path)
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        
        select_btn = QPushButton("选择图片")
        select_btn.clicked.connect(select_image)
        layout.addWidget(select_btn)
        
        # 美化选项
        layout.addWidget(QLabel("选择美化效果:"))
        
        effect_combo = QComboBox()
        effect_combo.addItems(["黑白滤镜", "复古滤镜", "模糊效果", "锐化效果", "边缘检测"])
        layout.addWidget(effect_combo)
        
        # 预览按钮
        def preview():
            if not image_path:
                QMessageBox.warning(None, "警告", "请先选择图片！")
                return
            
            try:
                # 打开图片
                img = Image.open(image_path)
                
                # 应用效果
                effect = effect_combo.currentText()
                
                if effect == "黑白滤镜":
                    img = img.convert("L").convert("RGB")
                elif effect == "复古滤镜":
                    # 简单复古效果：增加暖色调
                    r, g, b = img.split()
                    r = r.point(lambda x: min(x * 1.2, 255))
                    g = g.point(lambda x: min(x * 1.1, 255))
                    img = Image.merge("RGB", (r, g, b))
                elif effect == "模糊效果":
                    img = img.filter(ImageFilter.BLUR)
                elif effect == "锐化效果":
                    img = img.filter(ImageFilter.SHARPEN)
                elif effect == "边缘检测":
                    img = img.convert("L").filter(ImageFilter.FIND_EDGES)
                
                # 保存临时文件用于预览
                temp_path = "temp_avatar.jpg"
                img.save(temp_path)
                
                # 显示预览
                pixmap = QPixmap(temp_path)
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                
                # 保存美化后的图片
                output_path, _ = QFileDialog.getSaveFileName(
                    None,
                    "保存美化后的头像",
                    "beautified_avatar.jpg",
                    "JPEG Images (*.jpg);;PNG Images (*.png);;All Files (*)"
                )
                
                if output_path:
                    img.save(output_path)
                    QMessageBox.information(None, "成功", f"头像已保存到:\n{output_path}")
            
            except Exception as e:
                QMessageBox.warning(None, "错误", f"美化失败: {str(e)}")
        
        preview_btn = QPushButton("应用效果")
        preview_btn.clicked.connect(preview)
        layout.addWidget(preview_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def color_picker():
        """配色取色器"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("配色取色器")
        dialog.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(dialog)
        
        # 模式选择
        mode_combo = QComboBox()
        mode_combo.addItems(["从图片提取配色", "使用取色器", "预设配色方案"])
        layout.addWidget(QLabel("选择模式:"))
        layout.addWidget(mode_combo)
        
        # 结果展示
        result_layout = QHBoxLayout()
        
        # 颜色显示区域
        color_display = QLabel("选择模式开始")
        color_display.setAlignment(Qt.AlignCenter)
        color_display.setStyleSheet("font-size: 16px; padding: 20px; border: 1px solid #ccc;")
        color_display.setMinimumHeight(200)
        result_layout.addWidget(color_display)
        
        layout.addLayout(result_layout)
        
        # 功能实现
        def execute_mode():
            mode = mode_combo.currentText()
            
            if mode == "从图片提取配色":
                # 选择图片
                file_path, _ = QFileDialog.getOpenFileName(
                    None,
                    "选择图片",
                    "",
                    "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
                )
                
                if not file_path:
                    return
                
                try:
                    # 打开图片
                    img = Image.open(file_path)
                    
                    # 缩小图片以加快处理
                    img = img.resize((100, 100))
                    
                    # 获取主要颜色（简化版：取平均颜色）
                    pixels = list(img.getdata())
                    
                    # 统计颜色频率
                    from collections import Counter
                    color_counts = Counter(pixels)
                    most_common = color_counts.most_common(5)
                    
                    # 显示颜色
                    color_text = "提取的主要颜色（RGB）:\n\n"
                    for color, count in most_common:
                        color_text += f"RGB{color} - 出现{count}次\n"
                    
                    color_display.setText(color_text)
                    color_display.setStyleSheet("font-family: monospace; padding: 20px;")
                
                except Exception as e:
                    QMessageBox.warning(None, "错误", f"提取失败: {str(e)}")
            
            elif mode == "使用取色器":
                # 打开取色器
                color = QColorDialog.getColor()
                
                if color.isValid():
                    r, g, b = color.red(), color.green(), color.blue()
                    
                    # 显示颜色信息
                    color_text = f"""取色器结果:

RGB: ({r}, {g}, {b})
HEX: #{r:02X}{g:02X}{b:02X}
"""
                    
                    color_display.setText(color_text)
                    color_display.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); padding: 20px; color: {'#000' if r+g+b > 382 else '#FFF'};")
            
            else:  # 预设配色方案
                schemes = [
                    ("经典蓝白", ["#FFFFFF", "#2196F3", "#1976D2", "#0D47A1"]),
                    ("活力橙绿", ["#FFFFFF", "#FF9800", "#4CAF50", "#2E7D32"]),
                    ("少女粉紫", ["#FFFFFF", "#E91E63", "#9C27B0", "#6A1B9A"]),
                    ("商务灰蓝", ["#FFFFFF", "#607D8B", "#37474F", "#2196F3"]),
                ]
                
                scheme_name, colors = schemes[random.randint(0, len(schemes)-1)]
                
                color_text = f"预设配色方案: {scheme_name}\n\n"
                for hex_color in colors:
                    color_text += f"{hex_color}\n"
                
                color_display.setText(color_text)
                color_display.setStyleSheet("font-family: monospace; padding: 20px;")
        
        execute_btn = QPushButton("执行")
        execute_btn.clicked.connect(execute_mode)
        layout.addWidget(execute_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    # ==================== 文本生成工具 ====================
    
    @staticmethod
    def text_generator():
        """短句文案生成"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("短句文案生成")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 文案类型
        layout.addWidget(QLabel("选择文案类型:"))
        
        type_combo = QComboBox()
        type_combo.addItems(["朋友圈文案", "个性签名", "励志短句", "搞笑段子"])
        layout.addWidget(type_combo)
        
        # 生成按钮
        result_text = QTextEdit()
        result_text.setReadOnly(True)
        result_text.setPlaceholderText("生成的文案将显示在这里")
        layout.addWidget(result_text)
        
        def generate():
            """生成文案"""
            text_type = type_combo.currentText()
            
            # 文案库（简化版，实际应该从文件或API加载）
            templates = {
                "朋友圈文案": [
                    "今天的阳光特别温暖，就像你们给我的鼓励一样 ☀️",
                    "生活不止眼前的苟且，还有诗和远方 🌈",
                    "努力的人，运气不会太差 💪",
                    "每一次坚持，都是给自己最好的礼物 🎁",
                    "简单生活，快乐工作 ✨"
                ],
                "个性签名": [
                    "做一个温暖的人，不求大富大贵，但求无愧于心",
                    "人生没有彩排，每天都是现场直播",
                    "低调做人，高调做事",
                    "心若向阳，无畏悲伤",
                    "努力成为更好的自己"
                ],
                "励志短句": [
                    "不是因为看到希望才坚持，而是坚持了才有希望",
                    "成功不是将来才有的，而是从决定去做的那一刻起，持续累积而成",
                    "每一个不起舞的日子，都是对生命的辜负",
                    "只有不断找寻机会的人才会及时把握机会",
                    "行动是治愈恐惧的良药，而犹豫、拖延将不断滋养恐惧"
                ],
                "搞笑段子": [
                    "我是个低调的人，但在我心里，我很高调",
                    "我的优点是：我很帅；我的缺点是：我帅得不明显",
                    "人生就像一场旅行，在乎的不是目的地，而是堵车的路上",
                    "每天早上起床都要看一遍福布斯富豪榜，如果上面没有我的名字，我就去上班",
                    "我是个很宅的人，其实我也不想宅，只是没有地方去"
                ]
            }
            
            # 随机选择一条
            if text_type in templates:
                result = random.choice(templates[text_type])
                result_text.setText(result)
            else:
                result_text.setText("暂不支持该类型")
        
        generate_btn = QPushButton("生成文案")
        generate_btn.clicked.connect(generate)
        layout.addWidget(generate_btn)
        
        # 复制按钮
        copy_btn = QPushButton("复制到剪贴板")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(result_text.toPlainText()))
        layout.addWidget(copy_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def nickname_generator():
        """网名昵称设计"""
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("网名昵称设计")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 风格选择
        layout.addWidget(QLabel("选择昵称风格:"))
        
        style_combo = QComboBox()
        style_combo.addItems(["文艺清新", "高冷霸气", "可爱卖萌", "搞笑沙雕", "英文酷炫"])
        layout.addWidget(style_combo)
        
        # 关键词输入（可选）
        layout.addWidget(QLabel("输入关键词（可选，用空格分隔）:"))
        
        keyword_input = QLineEdit()
        keyword_input.setPlaceholderText("例如: 星辰 梦想 风")
        layout.addWidget(keyword_input)
        
        # 生成按钮
        result_text = QTextEdit()
        result_text.setReadOnly(True)
        result_text.setPlaceholderText("生成的昵称将显示在这里")
        layout.addWidget(result_text)
        
        def generate():
            """生成昵称"""
            style = style_combo.currentText()
            keywords = keyword_input.text().split() if keyword_input.text() else []
            
            # 昵称库（简化版）
            templates = {
                "文艺清新": [
                    "清风徐来", "星辰大海", "岁月静好", "云淡风轻", "心向远方",
                    "清风明月", "素年锦时", "一纸青春", "南风未起", "北暮苍穹"
                ],
                "高冷霸气": [
                    "一剑破苍穹", "笑看风云", "独孤求败", "王者归来", "傲视天下",
                    "冷月葬花魂", "剑指苍穹", "一念永恒", "逆天而行", "破碎虚空"
                ],
                "可爱卖萌": [
                    "软萌小兔", "甜心宝贝", "奶茶半糖", "草莓味的风", "会发光的星星",
                    "奶凶奶凶的", "小确幸", "元气少女", "软糯糯的团子", "银河投递员"
                ],
                "搞笑沙雕": [
                    "幼儿园扛把子", "精神小伙", "社会你龙哥", "网吧战神", "五行缺钱",
                    "秃头小可爱", "扶贫办主任", "幼儿园抢饭王", "精神病院院长", "躺平冠军"
                ],
                "英文酷炫": [
                    "Shadow", "Phoenix", "Storm", "Blaze", "Frost",
                    "Nightmare", "Legend", "Supreme", "Infinity", "Nebula"
                ]
            }
            
            # 生成昵称
            if style in templates:
                nicknames = templates[style]
                
                # 如果有关键词，尝试组合
                if keywords:
                    combined = []
                    for template in nicknames[:5]:  # 取前5个
                        for keyword in keywords:
                            combined.append(f"{keyword}_{template}")
                            combined.append(f"{template}_{keyword}")
                    nicknames = combined[:10]  # 限制数量
                else:
                    nicknames = random.sample(nicknames, min(10, len(nicknames)))
                
                # 显示结果
                result = "生成的昵称:\n\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(nicknames)])
                result_text.setText(result)
            else:
                result_text.setText("暂不支持该风格")
        
        generate_btn = QPushButton("生成昵称")
        generate_btn.clicked.connect(generate)
        layout.addWidget(generate_btn)
        
        # 复制按钮
        copy_btn = QPushButton("复制选中的昵称")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(result_text.toPlainText()))
        layout.addWidget(copy_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None


if __name__ == "__main__":
    # 测试
    tools = FunTools.get_tools()
    print(f"已加载 {len(tools)} 个趣味娱乐工具:")
    for tool in tools:
        print(f"  - {tool.icon} {tool.name}: {tool.description}")
