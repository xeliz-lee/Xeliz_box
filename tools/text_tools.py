#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理工具 - 完整工具模块
"""

import sys
import base64
from typing import Callable
from tools.base import Tool


class TextTools:
    """文本处理工具集"""
    
    @staticmethod
    def get_tools() -> list:
        """
        获取所有文本处理工具
        
        Returns:
            list: 工具列表
        """
        return [
            Tool(
                name="大小写转换",
                description="将文本转换为大写或小写",
                icon="🔤",
                tags=["文本", "大小写", "转换", "upper", "lower", "case"],
                execute_func=TextTools.case_convert
            ),
            Tool(
                name="字数统计",
                description="统计文本的字数、字符数、行数",
                icon="📊",
                tags=["文本", "字数", "统计", "count", "word", "char"],
                execute_func=TextTools.word_count
            ),
            Tool(
                name="繁简互换",
                description="繁体中文与简体中文互转",
                icon="🔄",
                tags=["文本", "繁体", "简体", "转换", "chinese", "traditional", "simplified"],
                execute_func=TextTools.traditional_convert
            ),
            Tool(
                name="二维码生成",
                description="将文本或URL生成二维码图片",
                icon="📱",
                tags=["二维码", "QR", "生成", "qrcode", "encode"],
                execute_func=TextTools.qrcode_generate
            ),
            Tool(
                name="二维码解析",
                description="从图片中解析二维码内容",
                icon="📷",
                tags=["二维码", "QR", "解析", "decode", "scan"],
                execute_func=TextTools.qrcode_decode
            ),
            Tool(
                name="密码生成",
                description="生成随机安全密码",
                icon="🔐",
                tags=["密码", "随机", "生成", "password", "random", "security"],
                execute_func=TextTools.password_generate
            ),
            Tool(
                name="文字排版",
                description="格式化文本（去除多余空格、空行等）",
                icon="📝",
                tags=["文本", "排版", "格式化", "format", "clean"],
                execute_func=TextTools.text_format
            ),
            Tool(
                name="文本加密",
                description="使用AES加密文本",
                icon="🔒",
                tags=["文本", "加密", "encrypt", "AES", "security"],
                execute_func=lambda: TextTools.text_encrypt_decrypt("encrypt")
            ),
            Tool(
                name="文本解密",
                description="解密AES加密的文本",
                icon="🔓",
                tags=["文本", "解密", "decrypt", "AES", "security"],
                execute_func=lambda: TextTools.text_encrypt_decrypt("decrypt")
            ),
        ]
    
    @staticmethod
    def case_convert():
        """大小写转换"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        
        # 获取输入文本
        text, ok = QInputDialog.getMultiLineText(
            None,
            "大小写转换",
            "请输入文本:",
            ""
        )
        
        if ok and text:
            # 选择转换类型
            options = ["转大写", "转小写", "首字母大写", "切换大小写"]
            choice, ok2 = QInputDialog.getItem(
                None,
                "选择转换类型",
                "请选择:",
                options,
                0,
                False
            )
            
            if ok2:
                if choice == "转大写":
                    result = text.upper()
                elif choice == "转小写":
                    result = text.lower()
                elif choice == "首字母大写":
                    result = text.title()
                elif choice == "切换大小写":
                    result = text.swapcase()
                else:
                    result = text
                
                # 显示结果
                msg_box = QMessageBox()
                msg_box.setWindowTitle("转换结果")
                msg_box.setText("转换成功！")
                msg_box.setDetailedText(result)
                msg_box.exec()
                
                # 复制到剪贴板
                from PySide6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(result)
                
                return result
        
        return None
    
    @staticmethod
    def word_count():
        """字数统计"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        
        # 获取输入文本
        text, ok = QInputDialog.getMultiLineText(
            None,
            "字数统计",
            "请输入文本:",
            ""
        )
        
        if ok and text:
            # 统计
            char_count = len(text)           # 字符数
            char_no_space = len(text.replace(" ", ""))  # 不含空格
            word_count = len(text.split())    # 单词数
            line_count = text.count("\n") + 1  # 行数
            chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')  # 中文字数
            
            # 显示结果
            result = f"""统计结果:
            
字符数（含空格）: {char_count}
字符数（不含空格）: {char_no_space}
单词数: {word_count}
行数: {line_count}
中文字数: {chinese_count}
"""
            QMessageBox.information(None, "字数统计", result)
            return result
        
        return None
    
    @staticmethod
    def traditional_convert():
        """繁简互换"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        
        try:
            from opencc import OpenCC
        except ImportError:
            QMessageBox.warning(None, "错误", "请先安装 opencc-python-reimplemented 库")
            return None
        
        # 获取输入文本
        text, ok = QInputDialog.getMultiLineText(
            None,
            "繁简互换",
            "请输入文本:",
            ""
        )
        
        if ok and text:
            # 选择转换方向
            options = ["繁体转简体", "简体转繁体"]
            choice, ok2 = QInputDialog.getItem(
                None,
                "选择转换方向",
                "请选择:",
                options,
                0,
                False
            )
            
            if ok2:
                try:
                    if choice == "繁体转简体":
                        cc = OpenCC('t2s')  # 繁体转简体
                    else:
                        cc = OpenCC('s2t')  # 简体转繁体
                    
                    result = cc.convert(text)
                    
                    # 显示结果
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("转换结果")
                    msg_box.setText("转换成功！")
                    msg_box.setDetailedText(result)
                    msg_box.exec()
                    
                    # 复制到剪贴板
                    from PySide6.QtWidgets import QApplication
                    clipboard = QApplication.clipboard()
                    clipboard.setText(result)
                    
                    return result
                except Exception as e:
                    QMessageBox.warning(None, "错误", f"转换失败: {str(e)}")
        
        return None
    
    @staticmethod
    def qrcode_generate():
        """二维码生成"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog
        
        try:
            import qrcode
            from PIL import ImageQt
            from PySide6.QtGui import QPixmap
        except ImportError:
            QMessageBox.warning(None, "错误", "请先安装 qrcode 和 pillow 库")
            return None
        
        # 获取输入文本
        text, ok = QInputDialog.getText(
            None,
            "二维码生成",
            "请输入文本或URL:",
            text=""
        )
        
        if ok and text:
            try:
                # 生成二维码
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(text)
                qr.make(fit=True)
                
                # 转换为图片
                img = qr.make_image(fill_color="black", back_color="white")
                
                # 保存文件
                file_path, _ = QFileDialog.getSaveFileName(
                    None,
                    "保存二维码",
                    "qrcode.png",
                    "PNG Images (*.png);;JPEG Images (*.jpg *.jpeg);;All Files (*)"
                )
                
                if file_path:
                    img.save(file_path)
                    QMessageBox.information(None, "成功", f"二维码已保存到:\n{file_path}")
                    return file_path
            except Exception as e:
                QMessageBox.warning(None, "错误", f"生成失败: {str(e)}")
        
        return None
    
    @staticmethod
    def qrcode_decode():
        """二维码解析"""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        
        try:
            from pyzbar.pyzbar import decode
            from PIL import Image
        except ImportError:
            QMessageBox.warning(None, "错误", "请先安装 pyzbar 和 pillow 库\npip install pyzbar pillow")
            return None
        
        # 选择图片文件
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择二维码图片",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        
        if file_path:
            try:
                # 读取图片
                img = Image.open(file_path)
                
                # 解析二维码
                decoded_objects = decode(img)
                
                if decoded_objects:
                    results = []
                    for obj in decoded_objects:
                        data = obj.data.decode('utf-8')
                        results.append(data)
                    
                    result_text = "\n\n".join(results)
                    
                    # 显示结果
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("解析结果")
                    msg_box.setText(f"找到 {len(decoded_objects)} 个二维码")
                    msg_box.setDetailedText(result_text)
                    msg_box.exec()
                    
                    # 复制到剪贴板
                    from PySide6.QtWidgets import QApplication
                    clipboard = QApplication.clipboard()
                    clipboard.setText(result_text)
                    
                    return result_text
                else:
                    QMessageBox.warning(None, "未找到", "图片中未找到二维码")
            except Exception as e:
                QMessageBox.warning(None, "错误", f"解析失败: {str(e)}")
        
        return None
    
    @staticmethod
    def password_generate():
        """密码生成"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        import random
        import string
        
        # 获取密码长度
        length, ok = QInputDialog.getInt(
            None,
            "密码生成",
            "请输入密码长度:",
            16,  # 默认值
            8,   # 最小值
            64,  # 最大值
            1    # 步长
        )
        
        if ok:
            # 选择字符集
            options = ["大写+小写+数字+符号", "大写+小写+数字", "大写+小写", "数字"]
            choice, ok2 = QInputDialog.getItem(
                None,
                "选择字符集",
                "请选择:",
                options,
                0,
                False
            )
            
            if ok2:
                # 构建字符集
                if choice == "大写+小写+数字+符号":
                    chars = string.ascii_letters + string.digits + string.punctuation
                elif choice == "大写+小写+数字":
                    chars = string.ascii_letters + string.digits
                elif choice == "大写+小写":
                    chars = string.ascii_letters
                elif choice == "数字":
                    chars = string.digits
                else:
                    chars = string.ascii_letters + string.digits
                
                # 生成密码
                password = ''.join(random.choice(chars) for _ in range(length))
                
                # 显示结果
                QMessageBox.information(None, "生成结果", f"密码:\n\n{password}")
                
                # 复制到剪贴板
                from PySide6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(password)
                
                return password
        
        return None
    
    @staticmethod
    def text_format():
        """文字排版"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        
        # 获取输入文本
        text, ok = QInputDialog.getMultiLineText(
            None,
            "文字排版",
            "请输入文本:",
            ""
        )
        
        if ok and text:
            # 选择格式化选项
            options = [
                "去除多余空格",
                "去除多余空行",
                "去除首尾空格",
                "全部（去除空格+空行+首尾空格）",
                "智能排版（段落格式化）"
            ]
            choice, ok2 = QInputDialog.getItem(
                None,
                "选择格式化类型",
                "请选择:",
                options,
                0,
                False
            )
            
            if ok2:
                try:
                    if choice == "去除多余空格":
                        # 多个空格合并为一个
                        import re
                        result = re.sub(r'\s+', ' ', text)
                    elif choice == "去除多余空行":
                        # 多个空行合并为一个
                        import re
                        result = re.sub(r'\n\s*\n+', '\n\n', text)
                    elif choice == "去除首尾空格":
                        # 去除每行首尾空格
                        result = '\n'.join(line.strip() for line in text.split('\n'))
                    elif choice == "全部（去除空格+空行+首尾空格）":
                        import re
                        # 去除首尾空格
                        result = '\n'.join(line.strip() for line in text.split('\n'))
                        # 去除多余空格
                        result = re.sub(r'\s+', ' ', result)
                        # 去除多余空行
                        result = re.sub(r'\n\s*\n+', '\n\n', result)
                    elif choice == "智能排版（段落格式化）":
                        import re
                        # 去除首尾空格
                        result = '\n'.join(line.strip() for line in text.split('\n'))
                        # 去除多余空格
                        result = re.sub(r'[ \t]+', ' ', result)
                        # 段落之间空一行
                        result = re.sub(r'([。！？\n])\s*\n(?=[^ \t\n])', r'\1\n\n', result)
                        # 去除多余空行
                        result = re.sub(r'\n{3,}', '\n\n', result)
                    else:
                        result = text
                    
                    # 显示结果
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("格式化结果")
                    msg_box.setText("格式化成功！")
                    msg_box.setDetailedText(result)
                    msg_box.exec()
                    
                    # 复制到剪贴板
                    from PySide6.QtWidgets import QApplication
                    clipboard = QApplication.clipboard()
                    clipboard.setText(result)
                    
                    return result
                except Exception as e:
                    QMessageBox.warning(None, "错误", f"格式化失败: {str(e)}")
        
        return None
    
    @staticmethod
    def text_encrypt_decrypt(mode: str):
        """文本加密/解密"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        
        try:
            from Crypto.Cipher import AES
            from Crypto.Random import get_random_bytes
            from Crypto.Util.Padding import pad, unpad
        except ImportError:
            QMessageBox.warning(None, "错误", "请先安装 pycryptodome 库\npip install pycryptodome")
            return None
        
        # 获取输入文本
        if mode == "encrypt":
            text, ok = QInputDialog.getMultiLineText(
                None,
                "文本加密",
                "请输入要加密的文本:",
                ""
            )
        else:
            text, ok = QInputDialog.getMultiLineText(
                None,
                "文本解密",
                "请输入要解密的文本（Base64格式）:",
                ""
            )
        
        if ok and text:
            try:
                if mode == "encrypt":
                    # 生成密钥（实际应用中应该从密码派生）
                    key = get_random_bytes(16)  # AES-128
                    
                    # 加密
                    cipher = AES.new(key, AES.MODE_CBC)
                    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
                    
                    # 组合IV和密文，然后Base64编码
                    result = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
                    
                    # 显示结果（包括密钥）
                    full_result = f"密钥（请保存，解密时需要）: {base64.b64encode(key).decode('utf-8')}\n\n密文:\n{result}"
                    
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("加密结果")
                    msg_box.setText("加密成功！请保存密钥和密文")
                    msg_box.setDetailedText(full_result)
                    msg_box.exec()
                    
                    # 复制到剪贴板
                    from PySide6.QtWidgets import QApplication
                    clipboard = QApplication.clipboard()
                    clipboard.setText(full_result)
                    
                    return full_result
                else:
                    # 解密
                    # 获取密钥
                    key_b64, ok2 = QInputDialog.getText(
                        None,
                        "输入密钥",
                        "请输入密钥（Base64格式）:",
                        text=""
                    )
                    
                    if ok2 and key_b64:
                        # 解码密钥和密文
                        key = base64.b64decode(key_b64)
                        enc_data = base64.b64decode(text)
                        
                        # 提取IV和密文
                        iv = enc_data[:16]
                        ct = enc_data[16:]
                        
                        # 解密
                        cipher = AES.new(key, AES.MODE_CBC, iv)
                        result = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
                        
                        # 显示结果
                        msg_box = QMessageBox()
                        msg_box.setWindowTitle("解密结果")
                        msg_box.setText("解密成功！")
                        msg_box.setDetailedText(result)
                        msg_box.exec()
                        
                        # 复制到剪贴板
                        from PySide6.QtWidgets import QApplication
                        clipboard = QApplication.clipboard()
                        clipboard.setText(result)
                        
                        return result
            except Exception as e:
                QMessageBox.warning(None, "错误", f"{'加密' if mode == 'encrypt' else '解密'}失败: {str(e)}")
        
        return None


if __name__ == "__main__":
    # 测试
    tools = TextTools.get_tools()
    print(f"已加载 {len(tools)} 个文本处理工具:")
    for tool in tools:
        print(f"  - {tool.icon} {tool.name}: {tool.description}")
