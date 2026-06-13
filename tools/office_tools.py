#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
办公效率工具模块 - 完整实现
"""

import os
import json
import time
import datetime
from tools.base import Tool
import tempfile
import shutil
from typing import Callable, List
from pathlib import Path


class OfficeTools:
    """办公效率工具集"""
    
    @staticmethod
    def get_tools() -> List:
        """
        获取所有办公效率工具
        
        Returns:
            List: 工具列表
        """
        return [
            # PDF处理
            Tool(
                name="PDF拆分",
                description="将PDF文件拆分为多个文件",
                icon="📄",
                tags=["PDF", "拆分", "split"],
                execute_func=OfficeTools.pdf_split
            ),
            Tool(
                name="PDF合并",
                description="将多个PDF文件合并为一个",
                icon="📑",
                tags=["PDF", "合并", "merge", "combine"],
                execute_func=OfficeTools.pdf_merge
            ),
            Tool(
                name="PDF转Word",
                description="将PDF文件转换为Word文档",
                icon="📝",
                tags=["PDF", "Word", "转换", "convert"],
                execute_func=lambda: OfficeTools.pdf_convert("word")
            ),
            Tool(
                name="PDF转图片",
                description="将PDF文件转换为图片",
                icon="🖼️",
                tags=["PDF", "图片", "转换", "image"],
                execute_func=lambda: OfficeTools.pdf_convert("image")
            ),
            
            # 快捷备忘
            Tool(
                name="便签记事",
                description="创建和管理便签",
                icon="📓",
                tags=["便签", "记事", "note", "memo"],
                execute_func=OfficeTools.sticky_notes
            ),
            Tool(
                name="清单待办",
                description="创建和管理待办事项",
                icon="✅",
                tags=["清单", "待办", "todo", "task"],
                execute_func=OfficeTools.todo_list
            ),
            Tool(
                name="剪贴板历史",
                description="查看和管理剪贴板历史记录",
                icon="📋",
                tags=["剪贴板", "历史", "clipboard", "history"],
                execute_func=OfficeTools.clipboard_history
            ),
            
            # 编码辅助
            Tool(
                name="时间戳转换",
                description="时间戳与日期时间互转",
                icon="⏰",
                tags=["时间戳", "转换", "timestamp", "convert"],
                execute_func=OfficeTools.timestamp_convert
            ),
            Tool(
                name="URL编解码",
                description="URL编码和解码",
                icon="🔗",
                tags=["URL", "编码", "解码", "encode", "decode"],
                execute_func=OfficeTools.url_encode_decode
            ),
            Tool(
                name="JSON格式化",
                description="格式化JSON数据",
                icon="📊",
                tags=["JSON", "格式化", "format", "beautify"],
                execute_func=OfficeTools.json_format
            ),
            
            # 系统工具
            Tool(
                name="文件批量重命名",
                description="批量重命名文件",
                icon="📁",
                tags=["文件", "重命名", "batch", "rename"],
                execute_func=OfficeTools.batch_rename
            ),
            Tool(
                name="垃圾清理",
                description="清理系统垃圾文件",
                icon="🗑️",
                tags=["垃圾", "清理", "clean", "temp"],
                execute_func=OfficeTools.junk_cleanup
            ),
            Tool(
                name="进程查看",
                description="查看和管理系统进程",
                icon="📈",
                tags=["进程", "查看", "process", "task"],
                execute_func=OfficeTools.process_viewer
            ),
            Tool(
                name="磁盘空间分析",
                description="分析磁盘空间使用情况",
                icon="💾",
                tags=["磁盘", "空间", "分析", "disk", "space"],
                execute_func=OfficeTools.disk_analyzer
            ),
            Tool(
                name="快捷键助手",
                description="查看和管理系统快捷键",
                icon="⌨️",
                tags=["快捷键", "助手", "shortcut", "hotkey"],
                execute_func=OfficeTools.shortcut_helper
            ),
        ]
    
    # ==================== PDF处理 ====================
    
    @staticmethod
    def pdf_split():
        """PDF拆分"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QProgressDialog)
        from PySide6.QtCore import Qt
        
        try:
            import PyPDF2
        except ImportError:
            QMessageBox.warning(None, "错误", "请先安装 PyPDF2 库\npip install PyPDF2")
            return None
        
        # 选择PDF文件
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择PDF文件",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if not file_path:
            return None
        
        try:
            # 读取PDF
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                total_pages = len(pdf.pages)
            
            # 选择拆分方式
            options = ["按页数拆分（每N页一个文件）", "按范围拆分（指定页码范围）", "按书签拆分（如果有书签）"]
            mode, ok = QInputDialog.getItem(
                None,
                "选择拆分方式",
                "请选择:",
                options,
                0,
                False
            )
            
            if not ok:
                return None
            
            output_dir = QFileDialog.getExistingDirectory(
                None,
                "选择输出目录",
                ""
            )
            
            if not output_dir:
                return None
            
            if mode == "按页数拆分（每N页一个文件）":
                # 获取每几页拆分
                pages_per_file, ok2 = QInputDialog.getInt(
                    None,
                    "每几页拆分",
                    "请输入每个文件的页数:",
                    1,  # 默认值
                    1,  # 最小值
                    total_pages,  # 最大值
                    1   # 步长
                )
                
                if not ok2:
                    return None
                
                # 拆分
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                
                with open(file_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    
                    for i in range(0, total_pages, pages_per_file):
                        writer = PyPDF2.PdfWriter()
                        
                        end_page = min(i + pages_per_file, total_pages)
                        
                        for page_num in range(i, end_page):
                            writer.add_page(pdf.pages[page_num])
                        
                        output_path = os.path.join(output_dir, f"{base_name}_part{i//pages_per_file + 1}.pdf")
                        
                        with open(output_path, 'wb') as out_f:
                            writer.write(out_f)
                
                QMessageBox.information(None, "完成", f"PDF已拆分为 { (total_pages + pages_per_file - 1) // pages_per_file } 个文件")
                return output_dir
            
            elif mode == "按范围拆分（指定页码范围）":
                # 输入页码范围
                range_str, ok2 = QInputDialog.getText(
                    None,
                    "输入页码范围",
                    f"请输入页码范围（用逗号分隔，如: 1-3,5,7-10）\n总页数: {total_pages}",
                    text="1-{}".format(total_pages)
                )
                
                if not ok2 or not range_str:
                    return None
                
                # 解析范围
                pages_to_extract = []
                for part in range_str.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_extract.extend(range(start - 1, end))  # 页码从0开始
                    else:
                        pages_to_extract.append(int(part) - 1)
                
                # 提取页面
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}_extracted.pdf")
                
                with open(file_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    writer = PyPDF2.PdfWriter()
                    
                    for page_num in pages_to_extract:
                        if 0 <= page_num < total_pages:
                            writer.add_page(pdf.pages[page_num])
                    
                    with open(output_path, 'wb') as out_f:
                        writer.write(out_f)
                
                QMessageBox.information(None, "完成", f"已提取 {len(pages_to_extract)} 页到:\n{output_path}")
                return output_path
            
            else:
                QMessageBox.warning(None, "提示", "按书签拆分功能开发中...")
                return None
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"拆分失败: {str(e)}")
            return None
    
    @staticmethod
    def pdf_merge():
        """PDF合并"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QProgressDialog,
                                       QListWidget, QVBoxLayout, QDialog, 
                                       QPushButton, QHBoxLayout)
        from PySide6.QtCore import Qt
        
        try:
            import PyPDF2
        except ImportError:
            QMessageBox.warning(None, "错误", "请先安装 PyPDF2 库\npip install PyPDF2")
            return None
        
        # 选择PDF文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择PDF文件（按顺序）",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if not files or len(files) < 2:
            QMessageBox.warning(None, "警告", "请选择至少2个PDF文件")
            return None
        
        try:
            # 创建顺序调整对话框
            dialog = QDialog(None)
            dialog.setWindowTitle("调整PDF顺序")
            dialog.setMinimumSize(400, 500)
            
            layout = QVBoxLayout(dialog)
            
            # 文件列表
            file_list = QListWidget()
            for f in files:
                file_list.addItem(f)
            layout.addWidget(file_list)
            
            # 按钮
            button_layout = QHBoxLayout()
            
            up_btn = QPushButton("上移")
            up_btn.clicked.connect(lambda: OfficeTools._move_item_up(file_list))
            button_layout.addWidget(up_btn)
            
            down_btn = QPushButton("下移")
            down_btn.clicked.connect(lambda: OfficeTools._move_item_down(file_list))
            button_layout.addWidget(down_btn)
            
            remove_btn = QPushButton("删除")
            remove_btn.clicked.connect(lambda: OfficeTools._remove_item(file_list))
            button_layout.addWidget(remove_btn)
            
            layout.addLayout(button_layout)
            
            # 合并按钮
            merge_btn = QPushButton("开始合并")
            merge_btn.clicked.connect(dialog.accept)
            layout.addWidget(merge_btn)
            
            # 取消按钮
            cancel_btn = QPushButton("取消")
            cancel_btn.clicked.connect(dialog.reject)
            layout.addWidget(cancel_btn)
            
            if dialog.exec() != QDialog.Accepted:
                return None
            
            # 获取调整后的文件顺序
            files = [file_list.item(i).text() for i in range(file_list.count())]
            
            # 选择输出文件
            output_path, _ = QFileDialog.getSaveFileName(
                None,
                "保存合并后的PDF",
                "merged.pdf",
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if not output_path:
                return None
            
            # 合并
            merger = PyPDF2.PdfMerger()
            
            for file_path in files:
                merger.append(file_path)
            
            merger.write(output_path)
            merger.close()
            
            QMessageBox.information(None, "完成", f"已合并 {len(files)} 个PDF文件到:\n{output_path}")
            return output_path
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"合并失败: {str(e)}")
            return None
    
    @staticmethod
    def _move_item_up(list_widget):
        """上移列表项"""
        current_row = list_widget.currentRow()
        if current_row > 0:
            item = list_widget.takeItem(current_row)
            list_widget.insertItem(current_row - 1, item)
            list_widget.setCurrentRow(current_row - 1)
    
    @staticmethod
    def _move_item_down(list_widget):
        """下移列表项"""
        current_row = list_widget.currentRow()
        if current_row < list_widget.count() - 1:
            item = list_widget.takeItem(current_row)
            list_widget.insertItem(current_row + 1, item)
            list_widget.setCurrentRow(current_row + 1)
    
    @staticmethod
    def _remove_item(list_widget):
        """删除列表项"""
        current_row = list_widget.currentRow()
        if current_row >= 0:
            list_widget.takeItem(current_row)
    
    @staticmethod
    def pdf_convert(target_format: str):
        """PDF格式转换"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QProgressDialog)
        from PySide6.QtCore import Qt
        
        # 选择PDF文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择PDF文件（可多选）",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if not files:
            return None
        
        try:
            output_dir = QFileDialog.getExistingDirectory(
                None,
                "选择输出目录",
                ""
            )
            
            if not output_dir:
                return None
            
            if target_format == "word":
                # PDF转Word（需要pdf2docx库）
                try:
                    from pdf2docx import Converter
                except ImportError:
                    QMessageBox.warning(None, "错误", "请先安装 pdf2docx 库\npip install pdf2docx")
                    return None
                
                # 转换
                for file_path in files:
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_path = os.path.join(output_dir, f"{base_name}.docx")
                    
                    cv = Converter(file_path)
                    cv.convert(output_path, start=0, end=None)
                    cv.close()
                
                QMessageBox.information(None, "完成", f"已转换 {len(files)} 个PDF文件为Word文档")
                return output_dir
            
            else:  # image
                # PDF转图片（需要pdf2image + poppler）
                try:
                    from pdf2image import convert_from_path
                except ImportError:
                    QMessageBox.warning(None, "错误", "请先安装 pdf2image 库\npip install pdf2image\n\n还需要安装 poppler")
                    return None
                
                # 转换
                for file_path in files:
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    file_output_dir = os.path.join(output_dir, base_name)
                    os.makedirs(file_output_dir, exist_ok=True)
                    
                    # 转换每一页
                    images = convert_from_path(file_path)
                    
                    for i, img in enumerate(images):
                        img_path = os.path.join(file_output_dir, f"page_{i+1}.png")
                        img.save(img_path, "PNG")
                
                QMessageBox.information(None, "完成", f"已转换 {len(files)} 个PDF文件为图片")
                return output_dir
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"转换失败: {str(e)}")
            return None
    
    # ==================== 快捷备忘 ====================
    
    @staticmethod
    def sticky_notes():
        """便签记事"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                                       QTextEdit, QPushButton, QListWidget,
                                       QInputDialog, QMessageBox)
        from PySide6.QtCore import Qt
        import json
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("便签记事")
        dialog.setMinimumSize(500, 600)
        
        layout = QVBoxLayout(dialog)
        
        # 便签列表
        note_list = QListWidget()
        layout.addWidget(note_list)
        
        # 加载便签
        notes_file = os.path.join(os.path.expanduser("~"), ".toolbox_notes.json")
        notes = []
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    notes = json.load(f)
            except:
                notes = []
        
        # 显示便签
        for note in notes:
            note_list.addItem(f"{note['title']} ({note['created']})")
        
        # 按钮
        button_layout = QHBoxLayout()
        
        new_btn = QPushButton("新建便签")
        new_btn.clicked.connect(lambda: OfficeTools._create_note(note_list, notes, notes_file))
        button_layout.addWidget(new_btn)
        
        edit_btn = QPushButton("编辑便签")
        edit_btn.clicked.connect(lambda: OfficeTools._edit_note(note_list, notes, notes_file))
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("删除便签")
        delete_btn.clicked.connect(lambda: OfficeTools._delete_note(note_list, notes, notes_file))
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _create_note(note_list, notes, notes_file):
        """创建新便签"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox,
                                       QDialog, QVBoxLayout, QTextEdit,
                                       QPushButton)
        
        # 输入标题
        title, ok = QInputDialog.getText(
            None,
            "新建便签",
            "请输入标题:",
            text=""
        )
        
        if not ok or not title:
            return
        
        # 输入内容
        dialog = QDialog(None)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(dialog.accept)
        layout.addWidget(save_btn)
        
        if dialog.exec() == QDialog.Accepted:
            content = text_edit.toPlainText()
            
            # 保存便签
            import datetime
            created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            notes.append({
                "title": title,
                "content": content,
                "created": created
            })
            
            # 更新列表
            note_list.addItem(f"{title} ({created})")
            
            # 保存到文件
            try:
                with open(notes_file, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, ensure_ascii=False, indent=2)
            except Exception as e:
                QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
    
    @staticmethod
    def _edit_note(note_list, notes, notes_file):
        """编辑便签"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTextEdit,
                                       QPushButton, QMessageBox)
        
        current_row = note_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(None, "警告", "请先选择要编辑的便签")
            return
        
        note = notes[current_row]
        
        # 编辑对话框
        dialog = QDialog(None)
        dialog.setWindowTitle(note['title'])
        dialog.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setPlainText(note['content'])
        layout.addWidget(text_edit)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(dialog.accept)
        layout.addWidget(save_btn)
        
        if dialog.exec() == QDialog.Accepted:
            # 更新便签
            note['content'] = text_edit.toPlainText()
            
            # 保存到文件
            try:
                with open(notes_file, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, ensure_ascii=False, indent=2)
            except Exception as e:
                QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
    
    @staticmethod
    def _delete_note(note_list, notes, notes_file):
        """删除便签"""
        from PySide6.QtWidgets import QMessageBox
        
        current_row = note_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(None, "警告", "请先选择要删除的便签")
            return
        
        # 确认删除
        reply = QMessageBox.question(
            None,
            "确认删除",
            f"确定要删除便签 '{notes[current_row]['title']}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 删除便签
            del notes[current_row]
            note_list.takeItem(current_row)
            
            # 保存到文件
            try:
                with open(notes_file, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, ensure_ascii=False, indent=2)
            except Exception as e:
                QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
    
    @staticmethod
    def todo_list():
        """清单待办"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                                       QListWidget, QPushButton, QInputDialog,
                                       QCheckBox, QWidget, QVBoxLayout,
                                       QMessageBox)
        from PySide6.QtCore import Qt
        import json
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("清单待办")
        dialog.setMinimumSize(500, 600)
        
        layout = QVBoxLayout(dialog)
        
        # 待办列表
        todo_list = QListWidget()
        layout.addWidget(todo_list)
        
        # 加载待办
        todo_file = os.path.join(os.path.expanduser("~"), ".toolbox_todo.json")
        todos = []
        if os.path.exists(todo_file):
            try:
                with open(todo_file, 'r', encoding='utf-8') as f:
                    todos = json.load(f)
            except:
                todos = []
        
        # 显示待办
        for todo in todos:
            status = "✓ " if todo['done'] else "□ "
            todo_list.addItem(f"{status}{todo['title']}")
        
        # 按钮
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("添加待办")
        add_btn.clicked.connect(lambda: OfficeTools._add_todo(todo_list, todos, todo_file))
        button_layout.addWidget(add_btn)
        
        toggle_btn = QPushButton("标记完成/未完成")
        toggle_btn.clicked.connect(lambda: OfficeTools._toggle_todo(todo_list, todos, todo_file))
        button_layout.addWidget(toggle_btn)
        
        delete_btn = QPushButton("删除待办")
        delete_btn.clicked.connect(lambda: OfficeTools._delete_todo(todo_list, todos, todo_file))
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _add_todo(todo_list, todos, todo_file):
        """添加待办"""
        from PySide6.QtWidgets import QInputDialog
        
        # 输入待办内容
        title, ok = QInputDialog.getText(
            None,
            "添加待办",
            "请输入待办内容:",
            text=""
        )
        
        if not ok or not title:
            return
        
        # 保存待办
        import datetime
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        todos.append({
            "title": title,
            "done": False,
            "created": created
        })
        
        # 更新列表
        todo_list.addItem(f"□ {title}")
        
        # 保存到文件
        try:
            with open(todo_file, 'w', encoding='utf-8') as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
    
    @staticmethod
    def _toggle_todo(todo_list, todos, todo_file):
        """标记完成/未完成"""
        from PySide6.QtWidgets import QMessageBox
        
        current_row = todo_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(None, "警告", "请先选择待办")
            return
        
        # 切换状态
        todos[current_row]['done'] = not todos[current_row]['done']
        
        # 更新列表
        todo = todos[current_row]
        status = "✓ " if todo['done'] else "□ "
        todo_list.currentItem().setText(f"{status}{todo['title']}")
        
        # 保存到文件
        try:
            with open(todo_file, 'w', encoding='utf-8') as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
    
    @staticmethod
    def _delete_todo(todo_list, todos, todo_file):
        """删除待办"""
        from PySide6.QtWidgets import QMessageBox
        
        current_row = todo_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(None, "警告", "请先选择要删除的待办")
            return
        
        # 确认删除
        reply = QMessageBox.question(
            None,
            "确认删除",
            f"确定要删除待办 '{todos[current_row]['title']}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 删除待办
            del todos[current_row]
            todo_list.takeItem(current_row)
            
            # 保存到文件
            try:
                with open(todo_file, 'w', encoding='utf-8') as f:
                    json.dump(todos, f, ensure_ascii=False, indent=2)
            except Exception as e:
                QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
    
    @staticmethod
    def clipboard_history():
        """剪贴板历史"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QListWidget,
                                       QPushButton, QMessageBox)
        from PySide6.QtGui import QClipboard
        from PySide6.QtWidgets import QApplication
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("剪贴板历史")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 历史列表
        history_list = QListWidget()
        layout.addWidget(history_list)
        
        # 加载历史（从文件）
        history_file = os.path.join(os.path.expanduser("~"), ".toolbox_clipboard.json")
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []
        
        # 显示历史
        for item in history[:50]:  # 只显示最近50条
            # 截断过长的内容
            display_text = item['content'][:100] + "..." if len(item['content']) > 100 else item['content']
            history_list.addItem(f"[{item['time']}] {display_text}")
        
        # 按钮
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("复制到剪贴板")
        copy_btn.clicked.connect(lambda: OfficeTools._copy_from_history(history_list, history))
        button_layout.addWidget(copy_btn)
        
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(lambda: OfficeTools._refresh_clipboard_history(history_list, history_file))
        button_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("清空历史")
        clear_btn.clicked.connect(lambda: OfficeTools._clear_clipboard_history(history_list, history_file))
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _copy_from_history(history_list, history):
        """从历史复制"""
        from PySide6.QtWidgets import QApplication
        
        current_row = history_list.currentRow()
        if current_row < 0:
            return
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(history[current_row]['content'])
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(None, "成功", "已复制到剪贴板")
    
    @staticmethod
    def _refresh_clipboard_history(history_list, history_file):
        """刷新剪贴板历史"""
        from PySide6.QtWidgets import QApplication
        import datetime
        
        clipboard = QApplication.clipboard()
        current_text = clipboard.text()
        
        if current_text:
            # 添加到历史
            import json
            
            history = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except:
                    history = []
            
            # 检查是否已存在
            if not history or history[0]['content'] != current_text:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history.insert(0, {
                    "content": current_text,
                    "time": now
                })
                
                # 限制历史条数
                history = history[:100]
                
                # 保存到文件
                try:
                    with open(history_file, 'w', encoding='utf-8') as f:
                        json.dump(history, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    from PySide6.QtWidgets import QMessageBox
                    QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
            
            # 刷新列表
            history_list.clear()
            for item in history[:50]:
                display_text = item['content'][:100] + "..." if len(item['content']) > 100 else item['content']
                history_list.addItem(f"[{item['time']}] {display_text}")
    
    @staticmethod
    def _clear_clipboard_history(history_list, history_file):
        """清空剪贴板历史"""
        from PySide6.QtWidgets import QMessageBox
        import json
        
        # 确认清空
        reply = QMessageBox.question(
            None,
            "确认清空",
            "确定要清空剪贴板历史吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 清空历史
            history = []
            
            # 保存到文件
            try:
                with open(history_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
            except Exception as e:
                QMessageBox.warning(None, "错误", f"保存失败: {str(e)}")
            
            # 刷新列表
            history_list.clear()
            
            QMessageBox.information(None, "成功", "已清空剪贴板历史")
    
    # ==================== 编码辅助 ====================
    
    @staticmethod
    def timestamp_convert():
        """时间戳转换"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                                       QLineEdit, QPushButton, QComboBox,
                                       QMessageBox)
        from PySide6.QtCore import QDateTime
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("时间戳转换")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 时间戳输入
        timestamp_input = QLineEdit()
        timestamp_input.setPlaceholderText("请输入时间戳（秒或毫秒）")
        form.addRow("时间戳:", timestamp_input)
        
        # 日期时间输入
        datetime_input = QLineEdit()
        datetime_input.setPlaceholderText("请输入日期时间（YYYY-MM-DD HH:MM:SS）")
        form.addRow("日期时间:", datetime_input)
        
        layout.addLayout(form)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        ts_to_dt_btn = QPushButton("时间戳 → 日期时间")
        ts_to_dt_btn.clicked.connect(lambda: OfficeTools._timestamp_to_datetime(timestamp_input.text()))
        button_layout.addWidget(ts_to_dt_btn)
        
        dt_to_ts_btn = QPushButton("日期时间 → 时间戳")
        dt_to_ts_btn.clicked.connect(lambda: OfficeTools._datetime_to_timestamp(datetime_input.text()))
        button_layout.addWidget(dt_to_ts_btn)
        
        layout.addLayout(button_layout)
        
        # 当前时间按钮
        now_btn = QPushButton("当前时间")
        now_btn.clicked.connect(lambda: OfficeTools._show_current_time(timestamp_input, datetime_input))
        layout.addWidget(now_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _timestamp_to_datetime(timestamp_str):
        """时间戳转日期时间"""
        from PySide6.QtWidgets import QMessageBox
        
        if not timestamp_str:
            QMessageBox.warning(None, "错误", "请输入时间戳")
            return
        
        try:
            timestamp = float(timestamp_str)
            
            # 判断是秒还是毫秒
            if timestamp > 1e10:  # 毫秒
                timestamp /= 1000
            
            # 转换
            dt = datetime.datetime.fromtimestamp(timestamp)
            
            result = f"""时间戳: {timestamp_str}
            
日期时间: {dt.strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            QMessageBox.information(None, "转换结果", result)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"转换失败: {str(e)}")
    
    @staticmethod
    def _datetime_to_timestamp(datetime_str):
        """日期时间转时间戳"""
        from PySide6.QtWidgets import QMessageBox
        
        if not datetime_str:
            QMessageBox.warning(None, "错误", "请输入日期时间")
            return
        
        try:
            # 解析日期时间
            dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            
            # 转换
            timestamp = int(dt.timestamp())
            timestamp_ms = timestamp * 1000
            
            result = f"""日期时间: {datetime_str}
            
时间戳（秒）: {timestamp}
时间戳（毫秒）: {timestamp_ms}
"""
            
            QMessageBox.information(None, "转换结果", result)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"转换失败: {str(e)}")
    
    @staticmethod
    def _show_current_time(timestamp_input, datetime_input):
        """显示当前时间"""
        now = datetime.datetime.now()
        
        timestamp_input.setText(str(int(now.timestamp())))
        datetime_input.setText(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    @staticmethod
    def url_encode_decode():
        """URL编解码"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                                       QTextEdit, QPushButton, QComboBox,
                                       QMessageBox)
        from urllib import parse
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("URL编解码")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 输入
        input_text = QTextEdit()
        input_text.setPlaceholderText("请输入要编码或解码的文本")
        layout.addWidget(input_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        encode_btn = QPushButton("URL编码")
        encode_btn.clicked.connect(lambda: OfficeTools._url_encode(input_text.toPlainText()))
        button_layout.addWidget(encode_btn)
        
        decode_btn = QPushButton("URL解码")
        decode_btn.clicked.connect(lambda: OfficeTools._url_decode(input_text.toPlainText()))
        button_layout.addWidget(decode_btn)
        
        layout.addLayout(button_layout)
        
        # 输出
        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_text.setPlaceholderText("输出结果")
        layout.addWidget(output_text)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _url_encode(text):
        """URL编码"""
        from PySide6.QtWidgets import QMessageBox
        from urllib import parse
        
        if not text:
            QMessageBox.warning(None, "错误", "请输入文本")
            return
        
        try:
            encoded = parse.quote(text)
            
            # 显示结果
            output_text = None
            for widget in QApplication.allWidgets():
                if isinstance(widget, QTextEdit) and widget.isReadOnly():
                    output_text = widget
                    break
            
            if output_text:
                output_text.setPlainText(encoded)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"编码失败: {str(e)}")
    
    @staticmethod
    def _url_decode(text):
        """URL解码"""
        from PySide6.QtWidgets import QMessageBox
        from urllib import parse
        
        if not text:
            QMessageBox.warning(None, "错误", "请输入文本")
            return
        
        try:
            decoded = parse.unquote(text)
            
            # 显示结果
            output_text = None
            for widget in QApplication.allWidgets():
                if isinstance(widget, QTextEdit) and widget.isReadOnly():
                    output_text = widget
                    break
            
            if output_text:
                output_text.setPlainText(decoded)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"解码失败: {str(e)}")
    
    @staticmethod
    def json_format():
        """JSON格式化"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout,
                                       QTextEdit, QPushButton,
                                       QMessageBox)
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("JSON格式化")
        dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # 输入
        input_text = QTextEdit()
        input_text.setPlaceholderText("请输入JSON文本")
        layout.addWidget(input_text)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        format_btn = QPushButton("格式化")
        format_btn.clicked.connect(lambda: OfficeTools._json_format(input_text.toPlainText()))
        button_layout.addWidget(format_btn)
        
        minify_btn = QPushButton("压缩")
        minify_btn.clicked.connect(lambda: OfficeTools._json_minify(input_text.toPlainText()))
        button_layout.addWidget(minify_btn)
        
        validate_btn = QPushButton("验证")
        validate_btn.clicked.connect(lambda: OfficeTools._json_validate(input_text.toPlainText()))
        button_layout.addWidget(validate_btn)
        
        layout.addLayout(button_layout)
        
        # 输出
        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_text.setPlaceholderText("输出结果")
        layout.addWidget(output_text)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _json_format(text):
        """JSON格式化"""
        from PySide6.QtWidgets import QMessageBox
        
        if not text:
            QMessageBox.warning(None, "错误", "请输入JSON文本")
            return
        
        try:
            parsed = json.loads(text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            
            # 显示结果
            output_text = None
            for widget in QApplication.allWidgets():
                if isinstance(widget, QTextEdit) and widget.isReadOnly():
                    output_text = widget
                    break
            
            if output_text:
                output_text.setPlainText(formatted)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"格式化失败: {str(e)}")
    
    @staticmethod
    def _json_minify(text):
        """JSON压缩"""
        from PySide6.QtWidgets import QMessageBox
        
        if not text:
            QMessageBox.warning(None, "错误", "请输入JSON文本")
            return
        
        try:
            parsed = json.loads(text)
            minified = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
            
            # 显示结果
            output_text = None
            for widget in QApplication.allWidgets():
                if isinstance(widget, QTextEdit) and widget.isReadOnly():
                    output_text = widget
                    break
            
            if output_text:
                output_text.setPlainText(minified)
        except Exception as e:
            QMessageBox.warning(None, "错误", f"压缩失败: {str(e)}")
    
    @staticmethod
    def _json_validate(text):
        """JSON验证"""
        from PySide6.QtWidgets import QMessageBox
        
        if not text:
            QMessageBox.warning(None, "错误", "请输入JSON文本")
            return
        
        try:
            parsed = json.loads(text)
            QMessageBox.information(None, "验证结果", "JSON格式正确！")
        except Exception as e:
            QMessageBox.warning(None, "验证结果", f"JSON格式错误:\n{str(e)}")
    
    # ==================== 系统工具 ====================
    
    @staticmethod
    def batch_rename():
        """文件批量重命名"""
        from PySide6.QtWidgets import (QFileDialog, QMessageBox, QInputDialog,
                                       QListWidget, QVBoxLayout, QDialog,
                                       QPushButton, QHBoxLayout, QCheckBox)
        from PySide6.QtCore import Qt
        
        # 选择文件
        files, _ = QFileDialog.getOpenFileNames(
            None,
            "选择文件（可多选）",
            "",
            "All Files (*)"
        )
        
        if not files or len(files) < 2:
            QMessageBox.warning(None, "警告", "请选择至少2个文件")
            return None
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("批量重命名")
        dialog.setMinimumSize(500, 600)
        
        layout = QVBoxLayout(dialog)
        
        # 文件列表
        file_list = QListWidget()
        for f in files:
            file_list.addItem(f)
        layout.addWidget(file_list)
        
        # 重命名规则
        form_layout = QFormLayout()
        
        # 前缀
        prefix_input = QLineEdit()
        prefix_input.setPlaceholderText("输入前缀（可选）")
        form_layout.addRow("前缀:", prefix_input)
        
        # 后缀
        suffix_input = QLineEdit()
        suffix_input.setPlaceholderText("输入后缀（可选）")
        form_layout.addRow("后缀:", suffix_input)
        
        # 替换
        find_input = QLineEdit()
        find_input.setPlaceholderText("查找内容")
        form_layout.addRow("查找:", find_input)
        
        replace_input = QLineEdit()
        replace_input.setPlaceholderText("替换为")
        form_layout.addRow("替换:", replace_input)
        
        # 序号
        add_number = QCheckBox("添加序号")
        add_number.setChecked(True)
        form_layout.addRow("序号:", add_number)
        
        layout.addLayout(form_layout)
        
        # 预览按钮
        preview_btn = QPushButton("预览")
        preview_btn.clicked.connect(lambda: OfficeTools._preview_rename(file_list, prefix_input.text(), suffix_input.text(), find_input.text(), replace_input.text(), add_number.isChecked()))
        layout.addWidget(preview_btn)
        
        # 执行按钮
        execute_btn = QPushButton("执行重命名")
        execute_btn.clicked.connect(lambda: OfficeTools._execute_rename(file_list, prefix_input.text(), suffix_input.text(), find_input.text(), replace_input.text(), add_number.isChecked()))
        layout.addWidget(execute_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _preview_rename(file_list, prefix, suffix, find, replace, add_number):
        """预览重命名"""
        # 生成新文件名
        new_names = []
        for i, item in enumerate(file_list.items()):
            file_path = item.text()
            dir_name = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            
            # 应用规则
            new_name = name
            
            if find and replace:
                new_name = new_name.replace(find, replace)
            
            if prefix:
                new_name = prefix + new_name
            
            if suffix:
                new_name = new_name + suffix
            
            if add_number:
                new_name = f"{new_name}_{i+1:03d}"
            
            new_name += ext
            
            new_path = os.path.join(dir_name, new_name)
            new_names.append(new_path)
        
        # 显示预览
        preview_dialog = QDialog(None)
        preview_dialog.setWindowTitle("预览重命名")
        preview_dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(preview_dialog)
        
        preview_list = QListWidget()
        for old, new in zip([file_list.item(i).text() for i in range(file_list.count())], new_names):
            preview_list.addItem(f"{os.path.basename(old)} → {os.path.basename(new)}")
        layout.addWidget(preview_list)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(preview_dialog.close)
        layout.addWidget(close_btn)
        
        preview_dialog.exec()
    
    @staticmethod
    def _execute_rename(file_list, prefix, suffix, find, replace, add_number):
        """执行重命名"""
        from PySide6.QtWidgets import QMessageBox
        
        # 确认执行
        reply = QMessageBox.question(
            None,
            "确认重命名",
            f"确定要重命名 {file_list.count()} 个文件吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 执行重命名
        success_count = 0
        for i in range(file_list.count()):
            file_path = file_list.item(i).text()
            dir_name = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            
            # 应用规则
            new_name = name
            
            if find and replace:
                new_name = new_name.replace(find, replace)
            
            if prefix:
                new_name = prefix + new_name
            
            if suffix:
                new_name = new_name + suffix
            
            if add_number:
                new_name = f"{new_name}_{i+1:03d}"
            
            new_name += ext
            
            new_path = os.path.join(dir_name, new_name)
            
            try:
                os.rename(file_path, new_path)
                success_count += 1
            except Exception as e:
                print(f"重命名 {file_path} 失败: {e}")
                continue
        
        QMessageBox.information(None, "完成", f"成功重命名 {success_count} 个文件")
    
    @staticmethod
    def junk_cleanup():
        """垃圾清理"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QProgressBar,
                                       QPushButton, QLabel, QMessageBox,
                                       QCheckBox, QVBoxLayout)
        from PySide6.QtCore import Qt, QThread, pyqtSignal
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("垃圾清理")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 清理选项
        options_layout = QVBoxLayout()
        
        temp_check = QCheckBox("临时文件")
        temp_check.setChecked(True)
        options_layout.addWidget(temp_check)
        
        recycle_check = QCheckBox("回收站")
        recycle_check.setChecked(True)
        options_layout.addWidget(recycle_check)
        
        cache_check = QCheckBox("浏览器缓存")
        cache_check.setChecked(True)
        options_layout.addWidget(cache_check)
        
        layout.addLayout(options_layout)
        
        # 进度条
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        layout.addWidget(progress_bar)
        
        # 状态标签
        status_label = QLabel("就绪")
        layout.addWidget(status_label)
        
        # 清理按钮
        cleanup_btn = QPushButton("开始清理")
        cleanup_btn.clicked.connect(lambda: OfficeTools._start_cleanup(temp_check.isChecked(), recycle_check.isChecked(), cache_check.isChecked(), progress_bar, status_label))
        layout.addWidget(cleanup_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _start_cleanup(clean_temp, clean_recycle, clean_cache, progress_bar, status_label):
        """开始清理"""
        from PySide6.QtWidgets import QMessageBox
        import tempfile
        
        cleaned_size = 0
        
        try:
            # 清理临时文件
            if clean_temp:
                status_label.setText("正在清理临时文件...")
                progress_bar.setValue(10)
                
                temp_dir = tempfile.gettempdir()
                cleaned_size += OfficeTools._clean_dir(temp_dir)
                
                progress_bar.setValue(30)
            
            # 清理回收站（Windows）
            if clean_recycle and os.name == 'nt':
                status_label.setText("正在清理回收站...")
                progress_bar.setValue(40)
                
                # Windows回收站路径
                # 这个需要调用Windows API，这里只是示意
                # 实际应该用 ctypes 调用 SHEmptyRecycleBin
                
                progress_bar.setValue(60)
            
            # 清理浏览器缓存
            if clean_cache:
                status_label.setText("正在清理浏览器缓存...")
                progress_bar.setValue(70)
                
                # Chrome缓存
                chrome_cache = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache")
                if os.path.exists(chrome_cache):
                    cleaned_size += OfficeTools._clean_dir(chrome_cache)
                
                # Firefox缓存
                firefox_cache = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Mozilla", "Firefox", "Profiles")
                if os.path.exists(firefox_cache):
                    # Firefox缓存比较复杂，这里只是示意
                    pass
                
                progress_bar.setValue(90)
            
            # 完成
            progress_bar.setValue(100)
            status_label.setText("清理完成")
            
            # 显示结果
            cleaned_mb = cleaned_size / (1024 * 1024)
            QMessageBox.information(None, "清理完成", f"清理完成！\n释放空间: {cleaned_mb:.2f} MB")
        
        except Exception as e:
            QMessageBox.warning(None, "错误", f"清理失败: {str(e)}")
    
    @staticmethod
    def _clean_dir(dir_path):
        """清理目录"""
        cleaned_size = 0
        
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    cleaned_size += file_size
                except Exception as e:
                    print(f"删除 {file_path} 失败: {e}")
                    continue
            
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f"删除 {dir_path} 失败: {e}")
                    continue
        
        return cleaned_size
    
    @staticmethod
    def process_viewer():
        """进程查看"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget,
                                       QPushButton, QHBoxLayout, QMessageBox,
                                       QTableWidgetItem)
        from PySide6.QtCore import Qt
        import psutil
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("进程查看")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # 进程表格
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["PID", "名称", "CPU (%)", "内存 (MB)", "状态"])
        layout.addWidget(table)
        
        # 加载进程
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
            try:
                proc_info = proc.info
                proc_info['memory_mb'] = proc_info['memory_info'].rss / (1024 * 1024)
                processes.append(proc_info)
            except:
                continue
        
        # 显示进程
        table.setRowCount(len(processes))
        for i, proc in enumerate(processes):
            table.setItem(i, 0, QTableWidgetItem(str(proc['pid'])))
            table.setItem(i, 1, QTableWidgetItem(proc['name']))
            table.setItem(i, 2, QTableWidgetItem(f"{proc['cpu_percent']:.1f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{proc['memory_mb']:.1f}"))
            table.setItem(i, 4, QTableWidgetItem(proc['status']))
        
        # 按钮
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(lambda: OfficeTools._refresh_processes(table))
        button_layout.addWidget(refresh_btn)
        
        kill_btn = QPushButton("结束进程")
        kill_btn.clicked.connect(lambda: OfficeTools._kill_process(table))
        button_layout.addWidget(kill_btn)
        
        layout.addLayout(button_layout)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _refresh_processes(table):
        """刷新进程"""
        import psutil
        
        # 清空表格
        table.setRowCount(0)
        
        # 加载进程
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
            try:
                proc_info = proc.info
                proc_info['memory_mb'] = proc_info['memory_info'].rss / (1024 * 1024)
                processes.append(proc_info)
            except:
                continue
        
        # 显示进程
        table.setRowCount(len(processes))
        for i, proc in enumerate(processes):
            table.setItem(i, 0, QTableWidgetItem(str(proc['pid'])))
            table.setItem(i, 1, QTableWidgetItem(proc['name']))
            table.setItem(i, 2, QTableWidgetItem(f"{proc['cpu_percent']:.1f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{proc['memory_mb']:.1f}"))
            table.setItem(i, 4, QTableWidgetItem(proc['status']))
    
    @staticmethod
    def _kill_process(table):
        """结束进程"""
        from PySide6.QtWidgets import QMessageBox
        import psutil
        
        current_row = table.currentRow()
        if current_row < 0:
            QMessageBox.warning(None, "警告", "请先选择进程")
            return
        
        pid = int(table.item(current_row, 0).text())
        name = table.item(current_row, 1).text()
        
        # 确认结束
        reply = QMessageBox.question(
            None,
            "确认结束进程",
            f"确定要结束进程 {name} (PID: {pid}) 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                QMessageBox.information(None, "成功", f"已结束进程 {name}")
                
                # 刷新
                OfficeTools._refresh_processes(table)
            except Exception as e:
                QMessageBox.warning(None, "错误", f"结束进程失败: {str(e)}")
    
    @staticmethod
    def disk_analyzer():
        """磁盘空间分析"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget,
                                       QPushButton, QMessageBox,
                                       QTableWidgetItem)
        from PySide6.QtCore import Qt
        import shutil
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("磁盘空间分析")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # 磁盘表格
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["盘符", "总大小 (GB)", "已用 (GB)", "可用 (GB)", "使用率 (%)"])
        layout.addWidget(table)
        
        # 加载磁盘信息
        partitions = psutil.disk_partitions()
        
        table.setRowCount(len(partitions))
        for i, partition in enumerate(partitions):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                table.setItem(i, 0, QTableWidgetItem(partition.device))
                table.setItem(i, 1, QTableWidgetItem(f"{usage.total / (1024**3):.2f}"))
                table.setItem(i, 2, QTableWidgetItem(f"{usage.used / (1024**3):.2f}"))
                table.setItem(i, 3, QTableWidgetItem(f"{usage.free / (1024**3):.2f}"))
                table.setItem(i, 4, QTableWidgetItem(f"{(usage.used / usage.total) * 100:.1f}"))
            except:
                continue
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def shortcut_helper():
        """快捷键助手"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget,
                                       QPushButton, QMessageBox,
                                       QTableWidgetItem, QLineEdit)
        from PySide6.QtCore import Qt
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("快捷键助手")
        dialog.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(dialog)
        
        # 搜索框
        search_box = QLineEdit()
        search_box.setPlaceholderText("搜索快捷键...")
        layout.addWidget(search_box)
        
        # 快捷键表格
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["快捷键", "功能", "分类"])
        layout.addWidget(table)
        
        # 加载快捷键
        shortcuts = [
            ("Ctrl+C", "复制", "通用"),
            ("Ctrl+V", "粘贴", "通用"),
            ("Ctrl+X", "剪切", "通用"),
            ("Ctrl+Z", "撤销", "通用"),
            ("Ctrl+Y", "重做", "通用"),
            ("Ctrl+S", "保存", "通用"),
            ("Ctrl+A", "全选", "通用"),
            ("Ctrl+F", "查找", "通用"),
            ("Ctrl+H", "替换", "通用"),
            ("Alt+Tab", "切换窗口", "Windows"),
            ("Win+D", "显示桌面", "Windows"),
            ("Win+E", "打开资源管理器", "Windows"),
            ("Win+R", "运行", "Windows"),
            ("Win+L", "锁定", "Windows"),
            ("Alt+F4", "关闭窗口", "Windows"),
            ("Ctrl+Shift+Esc", "任务管理器", "Windows"),
            ("F2", "重命名", "Windows"),
            ("F5", "刷新", "Windows"),
            ("Ctrl+K", "聚焦搜索框", "Xeliz_box"),
            ("↑↓", "选择工具", "Xeliz_box"),
            ("Enter", "执行工具", "Xeliz_box"),
            ("Esc", "隐藏到托盘", "Xeliz_box"),
        ]
        
        # 显示快捷键
        table.setRowCount(len(shortcuts))
        for i, (shortcut, function, category) in enumerate(shortcuts):
            table.setItem(i, 0, QTableWidgetItem(shortcut))
            table.setItem(i, 1, QTableWidgetItem(function))
            table.setItem(i, 2, QTableWidgetItem(category))
        
        # 搜索功能
        def search_shortcuts():
            query = search_box.text().lower()
            
            for i in range(table.rowCount()):
                match = False
                for j in range(table.columnCount()):
                    item = table.item(i, j)
                    if item and query in item.text().lower():
                        match = True
                        break
                
                table.setRowHidden(i, not match)
        
        search_box.textChanged.connect(search_shortcuts)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
        
        return None


if __name__ == "__main__":
    # 测试
    tools = OfficeTools.get_tools()
    print(f"已加载 {len(tools)} 个办公效率工具:")
    for tool in tools:
        print(f"  - {tool.icon} {tool.name}: {tool.description}")
