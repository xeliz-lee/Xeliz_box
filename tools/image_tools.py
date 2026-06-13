#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片工具模块 - 完整实现
"""

import os
import tempfile
from typing import Callable, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from tools.base import Tool
import pytesseract


class ImageTools:
    """图片工具集"""
    
    @staticmethod
    def get_tools() -> List:
        """
        获取所有图片处理工具
        
        Returns:
            List: 工具列表
        """
        return [
            Tool(
                name="图片压缩",
                description="压缩图片大小，支持批量处理",
                icon="🗜️",
                tags=["图片", "压缩", "image", "compress", "大小"],
                execute_func=ImageTools.compress_image
            ),
            Tool(
                name="格式转换",
                description="图片格式互转（PNG/JPG/WEBP/BMP）",
                icon="🔄",
                tags=["图片", "格式", "转换", "format", "png", "jpg", "webp"],
                execute_func=ImageTools.convert_format
            ),
            Tool(
                name="裁剪抠图",
                description="裁剪图片或去除背景",
                icon="✂️",
                tags=["图片", "裁剪", "抠图", "crop", "cut", "background"],
                execute_func=ImageTools.crop_image
            ),
            Tool(
                name="水印添加",
                description="给图片添加文字或图片水印",
                icon="💧",
                tags=["图片", "水印", "watermark", "text", "image"],
                execute_func=ImageTools.add_watermark
            ),
            Tool(
                name="长图拼接",
                description="将多张图片拼接成长图",
                icon="🖼️",
                tags=["图片", "拼接", "长图", "merge", "combine", "vertical"],
                execute_func=ImageTools.merge_images
            ),
            Tool(
                name="证件照换底色",
                description="更换证件照背景颜色（红/蓝/白/渐变）",
                icon="📸",
                tags=["图片", "证件照", "底色", "背景", "id", "photo"],
                execute_func=ImageTools.change_id_photo_bg
            ),
            Tool(
                name="图片OCR",
                description="从图片中提取文字（需安装Tesseract）",
                icon="📝",
                tags=["图片", "OCR", "文字识别", "text", "recognition", "extract"],
                execute_func=ImageTools.ocr_extract_text
            ),
        ]
    
    @staticmethod
    def compress_image():
        """图片压缩"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog, 
                                       QProgressDialog)
        from PySide6.QtCore import Qt
        
        # 选择图片文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择图片文件（可多选）",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp);;All Files (*)"
        )
        
        if not files:
            return None
        
        # 获取压缩质量
        quality, ok = QInputDialog.getInt(
            None,
            "压缩质量",
            "请输入压缩质量 (1-100):",
            85,  # 默认值
            1,   # 最小值
            100, # 最大值
            5    # 步长
        )
        
        if not ok:
            return None
        
        # 选择输出目录
        output_dir = QFileDialog.getExistingDirectory(
            None,
            "选择输出目录",
            ""
        )
        
        if not output_dir:
            return None
        
        try:
            # 创建进度对话框
            progress = QProgressDialog("正在压缩图片...", "取消", 0, len(files), None)
            progress.setWindowTitle("图片压缩")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            compressed_count = 0
            total_saved = 0
            
            for i, file_path in enumerate(files):
                progress.setValue(i)
                
                if progress.wasCanceled():
                    break
                
                try:
                    # 打开图片
                    img = Image.open(file_path)
                    
                    # 获取原始大小
                    original_size = os.path.getsize(file_path)
                    
                    # 生成输出文件路径
                    file_name = os.path.basename(file_path)
                    name, ext = os.path.splitext(file_name)
                    output_path = os.path.join(output_dir, f"{name}_compressed{ext}")
                    
                    # 压缩并保存
                    img.save(output_path, quality=quality, optimize=True)
                    
                    # 计算压缩后大小
                    compressed_size = os.path.getsize(output_path)
                    saved = original_size - compressed_size
                    total_saved += saved
                    
                    compressed_count += 1
                except Exception as e:
                    print(f"处理 {file_path} 失败: {e}")
                    continue
            
            progress.setValue(len(files))
            
            # 显示结果
            if compressed_count > 0:
                saved_mb = total_saved / (1024 * 1024)
                QMessageBox.information(
                    None,
                    "压缩完成",
                    f"成功压缩 {compressed_count} 张图片\n"
                    f"总节省空间: {saved_mb:.2f} MB"
                )
                return output_dir
            else:
                QMessageBox.warning(None, "警告", "没有成功压缩任何图片")
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"压缩失败: {str(e)}")
        
        return None
    
    @staticmethod
    def convert_format():
        """格式转换"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QProgressDialog)
        from PySide6.QtCore import Qt
        
        # 选择图片文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择图片文件（可多选）",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp *.gif);;All Files (*)"
        )
        
        if not files:
            return None
        
        # 选择目标格式
        formats = ["PNG", "JPEG", "WEBP", "BMP", "GIF"]
        target_format, ok = QInputDialog.getItem(
            None,
            "选择目标格式",
            "请选择目标格式:",
            formats,
            0,
            False
        )
        
        if not ok:
            return None
        
        # 选择输出目录
        output_dir = QFileDialog.getExistingDirectory(
            None,
            "选择输出目录",
            ""
        )
        
        if not output_dir:
            return None
        
        try:
            # 创建进度对话框
            progress = QProgressDialog("正在转换格式...", "取消", 0, len(files), None)
            progress.setWindowTitle("格式转换")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            converted_count = 0
            
            for i, file_path in enumerate(files):
                progress.setValue(i)
                
                if progress.wasCanceled():
                    break
                
                try:
                    # 打开图片
                    img = Image.open(file_path)
                    
                    # 如果是PNG/GIF等有透明通道的，需要转换为RGB（JPEG不支持透明）
                    if target_format in ["JPEG", "JPG"] and img.mode in ["RGBA", "P"]:
                        img = img.convert("RGB")
                    
                    # 生成输出文件路径
                    file_name = os.path.basename(file_path)
                    name, _ = os.path.splitext(file_name)
                    
                    # 根据格式确定扩展名
                    ext_map = {
                        "PNG": ".png",
                        "JPEG": ".jpg",
                        "WEBP": ".webp",
                        "BMP": ".bmp",
                        "GIF": ".gif"
                    }
                    
                    output_path = os.path.join(output_dir, f"{name}{ext_map[target_format]}")
                    
                    # 保存
                    img.save(output_path, format=target_format)
                    
                    converted_count += 1
                except Exception as e:
                    print(f"转换 {file_path} 失败: {e}")
                    continue
            
            progress.setValue(len(files))
            
            # 显示结果
            if converted_count > 0:
                QMessageBox.information(
                    None,
                    "转换完成",
                    f"成功转换 {converted_count} 张图片为 {target_format} 格式\n"
                    f"输出目录: {output_dir}"
                )
                return output_dir
            else:
                QMessageBox.warning(None, "警告", "没有成功转换任何图片")
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"转换失败: {str(e)}")
        
        return None
    
    @staticmethod
    def crop_image():
        """裁剪抠图"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QLabel, QVBoxLayout, QDialog, QPushButton,
                                       QHBoxLayout)
        from PySide6.QtGui import QPixmap
        from PySide6.QtCore import Qt
        
        # 选择图片文件
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择图片文件",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp);;All Files (*)"
        )
        
        if not file_path:
            return None
        
        try:
            # 打开图片
            img = Image.open(file_path)
            
            # 选择裁剪模式
            modes = ["矩形裁剪", "圆形裁剪", "自动抠图（简单背景移除）"]
            mode, ok = QInputDialog.getItem(
                None,
                "选择裁剪模式",
                "请选择:",
                modes,
                0,
                False
            )
            
            if not ok:
                return None
            
            # 裁剪对话框（简化版，实际应该用交互式裁剪）
            if mode == "矩形裁剪":
                # 输入裁剪区域
                rect_str, ok2 = QInputDialog.getText(
                    None,
                    "输入裁剪区域",
                    "请输入裁剪区域 (left,top,right,bottom):\n"
                    f"图片尺寸: {img.size[0]}x{img.size[1]}",
                    text=f"0,0,{img.size[0]},{img.size[1]}"
                )
                
                if ok2:
                    try:
                        # 解析坐标
                        coords = [int(x.strip()) for x in rect_str.split(",")]
                        if len(coords) != 4:
                            raise ValueError("需要4个坐标值")
                        
                        left, top, right, bottom = coords
                        
                        # 裁剪
                        img_cropped = img.crop((left, top, right, bottom))
                        
                        # 保存
                        output_path, _ = QFileDialog.getSaveFileName(
                            None,
                            "保存裁剪后的图片",
                            file_path.replace(".", "_cropped."),
                            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
                        )
                        
                        if output_path:
                            img_cropped.save(output_path)
                            QMessageBox.information(None, "成功", f"裁剪完成！\n保存至: {output_path}")
                            return output_path
                    except Exception as e:
                        QMessageBox.warning(None, "错误", f"裁剪失败: {str(e)}")
            
            elif mode == "圆形裁剪":
                # 创建圆形遮罩
                width, height = img.size
                mask = Image.new('L', (width, height), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, width, height), fill=255)
                
                # 应用遮罩
                img.putalpha(mask)
                
                # 保存
                output_path, _ = QFileDialog.getSaveFileName(
                    None,
                    "保存圆形裁剪后的图片",
                    file_path.replace(".", "_circle."),
                    "PNG Images (*.png);;All Files (*)"
                )
                
                if output_path:
                    img.save(output_path)
                    QMessageBox.information(None, "成功", f"圆形裁剪完成！\n保存至: {output_path}")
                    return output_path
            
            elif mode == "自动抠图（简单背景移除）":
                # 简单背景移除（使用阈值）
                # 更专业的做法是用 rembg 库，但这里用简单方法
                
                # 转换为RGBA
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                
                # 获取像素数据
                datas = img.getdata()
                
                # 创建新图片
                new_data = []
                for item in datas:
                    # 如果像素接近白色，设为透明
                    if item[0] > 240 and item[1] > 240 and item[2] > 240:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                
                img.putdata(new_data)
                
                # 保存
                output_path, _ = QFileDialog.getSaveFileName(
                    None,
                    "保存抠图后的图片",
                    file_path.replace(".", "_nobg."),
                    "PNG Images (*.png);;All Files (*)"
                )
                
                if output_path:
                    img.save(output_path)
                    QMessageBox.information(None, "成功", f"抠图完成！\n保存至: {output_path}\n\n注意：这是简单算法，复杂背景请用专业工具")
                    return output_path
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"裁剪失败: {str(e)}")
        
        return None
    
    @staticmethod
    def add_watermark():
        """水印添加"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QProgressDialog)
        from PySide6.QtCore import Qt
        from PIL import ImageDraw, ImageFont
        
        # 选择图片文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择图片文件（可多选）",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp);;All Files (*)"
        )
        
        if not files:
            return None
        
        # 选择水印类型
        types = ["文字水印", "图片水印"]
        watermark_type, ok = QInputDialog.getItem(
            None,
            "选择水印类型",
            "请选择:",
            types,
            0,
            False
        )
        
        if not ok:
            return None
        
        try:
            if watermark_type == "文字水印":
                # 输入水印文字
                text, ok2 = QInputDialog.getText(
                    None,
                    "输入水印文字",
                    "请输入水印文字:",
                    text="Sample Watermark"
                )
                
                if not ok2 or not text:
                    return None
                
                # 输入水印位置
                positions = ["左上", "右上", "左下", "右下", "居中"]
                position, ok3 = QInputDialog.getItem(
                    None,
                    "选择水印位置",
                    "请选择:",
                    positions,
                    4,  # 默认居中
                    False
                )
                
                if not ok3:
                    return None
                
                # 输入透明度
                opacity, ok4 = QInputDialog.getInt(
                    None,
                    "水印透明度",
                    "请输入透明度 (0-255, 0=完全透明):",
                    128,  # 默认值
                    0,    # 最小值
                    255,  # 最大值
                    10    # 步长
                )
                
                if not ok4:
                    return None
                
                # 处理图片
                for file_path in files:
                    try:
                        # 打开图片
                        img = Image.open(file_path)
                        
                        # 转换为RGBA
                        if img.mode != "RGBA":
                            img = img.convert("RGBA")
                        
                        # 创建水印层
                        watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
                        draw = ImageDraw.Draw(watermark_layer)
                        
                        # 尝试加载字体
                        try:
                            font = ImageFont.truetype("arial.ttf", 36)
                        except:
                            font = ImageFont.load_default()
                        
                        # 获取文字大小
                        bbox = draw.textbbox((0, 0), text, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        
                        # 计算位置
                        if position == "左上":
                            pos = (10, 10)
                        elif position == "右上":
                            pos = (img.size[0] - text_width - 10, 10)
                        elif position == "左下":
                            pos = (10, img.size[1] - text_height - 10)
                        elif position == "右下":
                            pos = (img.size[0] - text_width - 10, img.size[1] - text_height - 10)
                        else:  # 居中
                            pos = ((img.size[0] - text_width) // 2, (img.size[1] - text_height) // 2)
                        
                        # 绘制文字（带透明度）
                        draw.text(pos, text, font=font, fill=(255, 255, 255, opacity))
                        
                        # 合并图层
                        img_with_watermark = Image.alpha_composite(img, watermark_layer)
                        
                        # 保存
                        output_path = file_path.replace(".", "_watermark.")
                        img_with_watermark.save(output_path)
                    except Exception as e:
                        print(f"处理 {file_path} 失败: {e}")
                        continue
                
                QMessageBox.information(None, "完成", f"已添加文字水印到 {len(files)} 张图片")
                return files[0].replace(".", "_watermark.")
            
            else:  # 图片水印
                # 选择水印图片
                watermark_path, _ = QFileDialog.getOpenFileName(
                    None,
                    "选择水印图片（建议PNG带透明）",
                    "",
                    "PNG Images (*.png);;All Files (*)"
                )
                
                if not watermark_path:
                    return None
                
                # 打开水印图片
                watermark_img = Image.open(watermark_path)
                if watermark_img.mode != "RGBA":
                    watermark_img = watermark_img.convert("RGBA")
                
                # 处理图片
                for file_path in files:
                    try:
                        # 打开图片
                        img = Image.open(file_path)
                        
                        # 转换为RGBA
                        if img.mode != "RGBA":
                            img = img.convert("RGBA")
                        
                        # 调整水印大小（默认原图的1/4）
                        wm_width = img.size[0] // 4
                        wm_height = int(watermark_img.size[1] * (wm_width / watermark_img.size[0]))
                        watermark_resized = watermark_img.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
                        
                        # 计算位置（右下角）
                        pos = (img.size[0] - wm_width - 10, img.size[1] - wm_height - 10)
                        
                        # 合并图层
                        img.paste(watermark_resized, pos, watermark_resized)
                        
                        # 保存
                        output_path = file_path.replace(".", "_watermark.")
                        img.save(output_path)
                    except Exception as e:
                        print(f"处理 {file_path} 失败: {e}")
                        continue
                
                QMessageBox.information(None, "完成", f"已添加图片水印到 {len(files)} 张图片")
                return files[0].replace(".", "_watermark.")
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"添加水印失败: {str(e)}")
        
        return None
    
    @staticmethod
    def merge_images():
        """长图拼接"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QProgressDialog)
        from PySide6.QtCore import Qt
        
        # 选择图片文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择图片文件（按顺序排列）",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp);;All Files (*)"
        )
        
        if not files or len(files) < 2:
            QMessageBox.warning(None, "警告", "请选择至少2张图片")
            return None
        
        try:
            # 打开所有图片
            images = [Image.open(f) for f in files]
            
            # 选择拼接方向
            directions = ["垂直拼接（长图）", "水平拼接"]
            direction, ok = QInputDialog.getItem(
                None,
                "选择拼接方向",
                "请选择:",
                directions,
                0,
                False
            )
            
            if not ok:
                return None
            
            if direction == "垂直拼接（长图）":
                # 计算总高度和最大宽度
                total_height = sum(img.size[1] for img in images)
                max_width = max(img.size[0] for img in images)
                
                # 创建新图片
                merged = Image.new('RGB', (max_width, total_height), (255, 255, 255))
                
                # 拼接
                y_offset = 0
                for img in images:
                    # 如果宽度不一致，调整图片大小
                    if img.size[0] != max_width:
                        img = img.resize((max_width, int(img.size[1] * (max_width / img.size[0]))), Image.Resampling.LANCZOS)
                    
                    merged.paste(img, (0, y_offset))
                    y_offset += img.size[1]
            else:
                # 计算总宽度和最大高度
                total_width = sum(img.size[0] for img in images)
                max_height = max(img.size[1] for img in images)
                
                # 创建新图片
                merged = Image.new('RGB', (total_width, max_height), (255, 255, 255))
                
                # 拼接
                x_offset = 0
                for img in images:
                    # 如果高度不一致，调整图片大小
                    if img.size[1] != max_height:
                        img = img.resize((int(img.size[0] * (max_height / img.size[1])), max_height), Image.Resampling.LANCZOS)
                    
                    merged.paste(img, (x_offset, 0))
                    x_offset += img.size[0]
            
            # 保存
            output_path, _ = QFileDialog.getSaveFileName(
                None,
                "保存拼接后的图片",
                "merged.png",
                "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
            )
            
            if output_path:
                merged.save(output_path)
                QMessageBox.information(None, "成功", f"拼接完成！\n保存至: {output_path}")
                return output_path
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"拼接失败: {str(e)}")
        
        return None
    
    @staticmethod
    def change_id_photo_bg():
        """证件照换底色"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QLabel, QVBoxLayout, QDialog)
        from PySide6.QtGui import QPixmap
        from PySide6.QtCore import Qt
        
        # 选择图片文件
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择证件照",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if not file_path:
            return None
        
        try:
            # 打开图片
            img = Image.open(file_path)
            
            # 转换为RGBA
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            
            # 选择目标底色
            colors = ["白色", "蓝色", "红色", "渐变蓝色"]
            color, ok = QInputDialog.getItem(
                None,
                "选择目标底色",
                "请选择:",
                colors,
                0,
                False
            )
            
            if not ok:
                return None
            
            # 定义颜色映射
            color_map = {
                "白色": (255, 255, 255),
                "蓝色": (0, 123, 194),
                "红色": (255, 0, 0),
            }
            
            if color in color_map:
                target_color = color_map[color]
                
                # 获取像素数据
                datas = img.getdata()
                
                # 创建新图片
                new_data = []
                for item in datas:
                    # 如果像素接近白色或浅色，替换为目标色
                    if item[0] > 200 and item[1] > 200 and item[2] > 200:
                        new_data.append((target_color[0], target_color[1], target_color[2], item[3]))
                    else:
                        new_data.append(item)
                
                img.putdata(new_data)
            else:
                # 渐变蓝色（从上到下：浅蓝到深蓝）
                width, height = img.size
                datas = img.getdata()
                new_data = []
                
                for y in range(height):
                    for x in range(width):
                        idx = y * width + x
                        item = datas[idx]
                        
                        # 计算渐变（y/height从0到1）
                        ratio = y / height
                        r = int(135 + (0 - 135) * ratio)      # 135 -> 0
                        g = int(206 + (123 - 206) * ratio)    # 206 -> 123
                        b = int(250 + (194 - 250) * ratio)    # 250 -> 194
                        
                        # 如果像素接近白色，替换为渐变色
                        if item[0] > 200 and item[1] > 200 and item[2] > 200:
                            new_data.append((r, g, b, item[3]))
                        else:
                            new_data.append(item)
                
                img.putdata(new_data)
            
            # 保存
            output_path, _ = QFileDialog.getSaveFileName(
                None,
                "保存换底色后的证件照",
                file_path.replace(".", "_newbg."),
                "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
            )
            
            if output_path:
                # 如果是JPEG，需要转换为RGB
                if output_path.endswith((".jpg", ".jpeg")):
                    img = img.convert("RGB")
                
                img.save(output_path)
                QMessageBox.information(None, "成功", f"换底色完成！\n保存至: {output_path}")
                return output_path
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"换底色失败: {str(e)}")
        
        return None
    
    @staticmethod
    def ocr_extract_text():
        """图片OCR - 提取文字"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QProgressDialog, QTextEdit)
        from PySide6.QtCore import Qt
        
        # 检查Tesseract是否安装
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            QMessageBox.warning(
                None,
                "错误",
                "未检测到 Tesseract OCR 引擎\n\n"
                "请先安装：\n"
                "1. 下载 Tesseract: https://github.com/tesseract-ocr/tesseract\n"
                "2. 安装中文语言包\n"
                "3. 设置环境变量 TESSDATA_PREFIX 指向 tessdata 目录"
            )
            return None
        
        # 选择图片文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择图片文件（可多选）",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff);;All Files (*)"
        )
        
        if not files:
            return None
        
        try:
            # 选择语言
            languages = ["chi_sim+eng (简体中文+英文)", "chi_tra+eng (繁体中文+英文)", "eng (英文)", "jpn (日文)"]
            language, ok = QInputDialog.getItem(
                None,
                "选择识别语言",
                "请选择:",
                languages,
                0,
                False
            )
            
            if not ok:
                return None
            
            # 解析语言代码
            lang_code = language.split(" ")[0]
            
            # 创建进度对话框
            progress = QProgressDialog("正在识别文字...", "取消", 0, len(files), None)
            progress.setWindowTitle("OCR识别")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            all_text = []
            
            for i, file_path in enumerate(files):
                progress.setValue(i)
                
                if progress.wasCanceled():
                    break
                
                try:
                    # 打开图片
                    img = Image.open(file_path)
                    
                    # OCR识别
                    text = pytesseract.image_to_string(img, lang=lang_code)
                    
                    all_text.append(f"=== {os.path.basename(file_path)} ===\n{text}\n")
                except Exception as e:
                    all_text.append(f"=== {os.path.basename(file_path)} ===\n识别失败: {str(e)}\n")
                    continue
            
            progress.setValue(len(files))
            
            # 显示结果
            result_text = "\n".join(all_text)
            
            # 创建结果对话框
            dialog = QDialog(None)
            dialog.setWindowTitle("OCR识别结果")
            dialog.setMinimumSize(600, 400)
            
            layout = QVBoxLayout(dialog)
            
            text_edit = QTextEdit()
            text_edit.setPlainText(result_text)
            text_edit.setReadOnly(True)
            layout.addWidget(text_edit)
            
            # 按钮
            button_layout = QHBoxLayout()
            
            copy_button = QPushButton("复制到剪贴板")
            copy_button.clicked.connect(lambda: QApplication.clipboard().setText(result_text))
            button_layout.addWidget(copy_button)
            
            save_button = QPushButton("保存为文本文件")
            save_button.clicked.connect(lambda: ImageTools._save_ocr_result(result_text))
            button_layout.addWidget(save_button)
            
            close_button = QPushButton("关闭")
            close_button.clicked.connect(dialog.close)
            button_layout.addWidget(close_button)
            
        except Exception as e:
            QMessageBox.warning(None, "错误", f"OCR识别失败: {str(e)}")
        
        return None
    
    @staticmethod
    def _save_ocr_result(text: str):
        """保存OCR结果到文件"""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "保存OCR结果",
            "ocr_result.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                QMessageBox.information(None, "成功", f"结果已保存到:\n{file_path}")
                return file_path
            except Exception as e:
                QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
        
        return None


if __name__ == "__main__":
    # 测试
    tools = ImageTools.get_tools()
    print(f"已加载 {len(tools)} 个图片处理工具:")
    for tool in tools:
        print(f"  - {tool.icon} {tool.name}: {tool.description}")
