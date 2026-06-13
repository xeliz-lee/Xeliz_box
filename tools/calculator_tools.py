#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算器工具模块 - 完整实现
"""

import re
import math
from datetime import datetime, timedelta
from typing import Callable, List
from tools.base import Tool


class CalculatorTools:
    """计算器工具集"""
    
    @staticmethod
    def get_tools() -> List:
        """
        获取所有计算器工具
        
        Returns:
            List: 工具列表
        """
        return [
            Tool(
                name="常规计算器",
                description="基础四则运算和科学计算",
                icon="🧮",
                tags=["计算器", "计算", "calculator", "math", "基础"],
                execute_func=CalculatorTools.basic_calculator
            ),
            Tool(
                name="房贷计算器",
                description="计算房贷月供、总利息",
                icon="🏠",
                tags=["计算器", "房贷", "mortgage", "贷款", "月供"],
                execute_func=CalculatorTools.mortgage_calculator
            ),
            Tool(
                name="车贷计算器",
                description="计算车贷月供、总利息",
                icon="🚗",
                tags=["计算器", "车贷", "car", "loan", "贷款"],
                execute_func=CalculatorTools.car_loan_calculator
            ),
            Tool(
                name="个税计算器",
                description="计算个人所得税",
                icon="💰",
                tags=["计算器", "个税", "tax", "所得税", "收入"],
                execute_func=CalculatorTools.income_tax_calculator
            ),
            Tool(
                name="进制换算",
                description="二进制/八进制/十进制/十六进制互转",
                icon="🔢",
                tags=["计算器", "进制", "转换", "binary", "hex", "decimal"],
                execute_func=CalculatorTools.base_conversion
            ),
            Tool(
                name="日期倒计时",
                description="计算两个日期之间的天数",
                icon="📅",
                tags=["计算器", "日期", "倒计时", "days", "countdown"],
                execute_func=CalculatorTools.date_countdown
            ),
            Tool(
                name="年龄天数计算",
                description="计算年龄或两个日期之间的天数",
                icon="🎂",
                tags=["计算器", "年龄", "天数", "age", "days"],
                execute_func=CalculatorTools.age_calculator
            ),
            Tool(
                name="单位换算",
                description="长度/重量/体积/网速单位互转",
                icon="📏",
                tags=["计算器", "单位", "换算", "convert", "unit"],
                execute_func=CalculatorTools.unit_conversion
            ),
        ]
    
    @staticmethod
    def basic_calculator():
        """常规计算器"""
        from PySide6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout,
                                       QPushButton, QLineEdit, QMessageBox)
        from PySide6.QtCore import Qt
        
        # 创建计算器对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("常规计算器")
        dialog.setMinimumSize(300, 400)
        
        # 布局
        layout = QVBoxLayout(dialog)
        
        # 显示屏
        display = QLineEdit()
        display.setReadOnly(True)
        display.setAlignment(Qt.AlignRight)
        display.setMaxLength(15)
        display.setText("0")
        display.setStyleSheet("font-size: 20px; padding: 5px;")
        layout.addWidget(display)
        
        # 按钮网格
        grid = QGridLayout()
        
        # 按钮定义
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('CE', 4, 1), ('←', 4, 2), ('%', 4, 3),
        ]
        
        # 创建按钮
        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            button.setMinimumSize(50, 50)
            button.setStyleSheet("font-size: 16px;")
            grid.addWidget(button, row, col)
            
            # 连接信号
            if btn_text == '=':
                button.clicked.connect(lambda: CalculatorTools._calculate(display))
            elif btn_text == 'C':
                button.clicked.connect(lambda: display.clear() or display.setText('0'))
            elif btn_text == 'CE':
                button.clicked.connect(lambda: display.setText('0'))
            elif btn_text == '←':
                button.clicked.connect(lambda: display.setText(display.text()[:-1]) or (display.setText('0') if not display.text() else None))
            elif btn_text == '%':
                button.clicked.connect(lambda: CalculatorTools._percentage(display))
            else:
                button.clicked.connect(lambda checked, text=btn_text: CalculatorTools._button_clicked(display, text))
        
        layout.addLayout(grid)
        dialog.exec()
        
        return display.text()
    
    @staticmethod
    def _button_clicked(display, text):
        """计算器按钮点击"""
        if display.text() == '0':
            display.setText(text)
        else:
            display.insert(text)
    
    @staticmethod
    def _calculate(display):
        """计算公式"""
        try:
            result = eval(display.text())
            display.setText(str(result))
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(None, "错误", f"计算失败: {str(e)}")
    
    @staticmethod
    def _percentage(display):
        """百分比"""
        try:
            value = float(display.text())
            display.setText(str(value / 100))
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(None, "错误", f"计算失败: {str(e)}")
    
    @staticmethod
    def mortgage_calculator():
        """房贷计算器"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QDoubleSpinBox,
                                       QPushButton, QRadioButton, QButtonGroup)
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("房贷计算器")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 贷款总额
        loan_amount = QDoubleSpinBox()
        loan_amount.setRange(1, 10000)  # 1万到1亿
        loan_amount.setSuffix(" 万元")
        loan_amount.setValue(100)
        loan_amount.setSingleStep(1)
        form.addRow("贷款总额:", loan_amount)
        
        # 贷款年限
        loan_years = QDoubleSpinBox()
        loan_years.setRange(1, 30)
        loan_years.setValue(30)
        loan_years.setSuffix(" 年")
        form.addRow("贷款年限:", loan_years)
        
        # 贷款利率
        interest_rate = QDoubleSpinBox()
        interest_rate.setRange(1, 10)
        interest_rate.setValue(4.2)
        interest_rate.setSuffix(" %")
        interest_rate.setSingleStep(0.1)
        interest_rate.setDecimals(2)
        form.addRow("贷款利率:", interest_rate)
        
        # 还款方式
        repayment_group = QButtonGroup(dialog)
        repayment_layout = QHBoxLayout()
        
        equal_installment = QRadioButton("等额本息")
        equal_installment.setChecked(True)
        repayment_group.addButton(equal_installment, 0)
        repayment_layout.addWidget(equal_installment)
        
        equal_principal = QRadioButton("等额本金")
        repayment_group.addButton(equal_principal, 1)
        repayment_layout.addWidget(equal_principal)
        
        form.addRow("还款方式:", repayment_layout)
        
        layout.addLayout(form)
        
        # 计算按钮
        calculate_btn = QPushButton("计算")
        calculate_btn.clicked.connect(lambda: CalculatorTools._calc_mortgage(
            loan_amount.value(),
            loan_years.value(),
            interest_rate.value(),
            equal_installment.isChecked()
        ))
        layout.addWidget(calculate_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _calc_mortgage(amount_wan, years, rate_percent, is_equal_installment):
        """计算房贷"""
        from PySide6.QtWidgets import QMessageBox
        
        # 转换单位
        amount = amount_wan * 10000  # 万元转元
        monthly_rate = rate_percent / 100 / 12  # 月利率
        months = int(years * 12)  # 总月数
        
        if is_equal_installment:
            # 等额本息
            if monthly_rate == 0:
                monthly_payment = amount / months
            else:
                monthly_payment = amount * monthly_rate * pow(1 + monthly_rate, months) / (pow(1 + monthly_rate, months) - 1)
            
            total_payment = monthly_payment * months
            total_interest = total_payment - amount
            
            result = f"""等额本息还款方式:
            
贷款总额: {amount_wan:.2f} 万元 ({amount:.2f} 元)
贷款年限: {years} 年 ({months} 个月)
贷款利率: {rate_percent:.2f}%

月供: {monthly_payment:.2f} 元
总还款: {total_payment:.2f} 元
总利息: {total_interest:.2f} 元
"""
        else:
            # 等额本金
            monthly_principal = amount / months
            total_interest = 0
            
            result = f"""等额本金还款方式:
            
贷款总额: {amount_wan:.2f} 万元 ({amount:.2f} 元)
贷款年限: {years} 年 ({months} 个月)
贷款利率: {rate_percent:.2f}%

首月还款: {monthly_principal + amount * monthly_rate:.2f} 元
每月递减: {monthly_principal * monthly_rate:.2f} 元
"""
            
            # 计算总利息
            for i in range(months):
                remaining = amount - monthly_principal * i
                interest = remaining * monthly_rate
                total_interest += interest
            
            total_payment = amount + total_interest
            
            result += f"""
总还款: {total_payment:.2f} 元
总利息: {total_interest:.2f} 元
"""
        
        QMessageBox.information(None, "房贷计算结果", result)
        return result
    
    @staticmethod
    def car_loan_calculator():
        """车贷计算器"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QDoubleSpinBox,
                                       QPushButton, QComboBox)
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("车贷计算器")
        dialog.setMinimumSize(400, 250)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 车价
        car_price = QDoubleSpinBox()
        car_price.setRange(1, 1000)
        car_price.setSuffix(" 万元")
        car_price.setValue(15)
        car_price.setSingleStep(1)
        form.addRow("车价:", car_price)
        
        # 首付比例
        down_payment_rate = QDoubleSpinBox()
        down_payment_rate.setRange(0, 90)
        down_payment_rate.setValue(30)
        down_payment_rate.setSuffix(" %")
        down_payment_rate.setSingleStep(5)
        form.addRow("首付比例:", down_payment_rate)
        
        # 贷款年限
        loan_years = QComboBox()
        loan_years.addItems(["1年", "2年", "3年", "4年", "5年"])
        loan_years.setCurrentIndex(2)  # 默认3年
        form.addRow("贷款年限:", loan_years)
        
        # 贷款利率
        interest_rate = QDoubleSpinBox()
        interest_rate.setRange(1, 10)
        interest_rate.setValue(3.5)
        interest_rate.setSuffix(" %")
        interest_rate.setSingleStep(0.1)
        interest_rate.setDecimals(2)
        form.addRow("贷款利率:", interest_rate)
        
        layout.addLayout(form)
        
        # 计算按钮
        calculate_btn = QPushButton("计算")
        calculate_btn.clicked.connect(lambda: CalculatorTools._calc_car_loan(
            car_price.value(),
            down_payment_rate.value() / 100,
            int(loan_years.currentText()[:-1]),
            interest_rate.value()
        ))
        layout.addWidget(calculate_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _calc_car_loan(price_wan, down_payment_ratio, years, rate_percent):
        """计算车贷"""
        from PySide6.QtWidgets import QMessageBox
        
        # 转换单位
        price = price_wan * 10000  # 万元转元
        down_payment = price * down_payment_ratio
        loan_amount = price - down_payment
        monthly_rate = rate_percent / 100 / 12
        months = years * 12
        
        # 等额本息
        if monthly_rate == 0:
            monthly_payment = loan_amount / months
        else:
            monthly_payment = loan_amount * monthly_rate * pow(1 + monthly_rate, months) / (pow(1 + monthly_rate, months) - 1)
        
        total_payment = down_payment + monthly_payment * months
        total_interest = monthly_payment * months - loan_amount
        
        result = f"""车贷计算结果:
        
车价: {price_wan:.2f} 万元 ({price:.2f} 元)
首付: {down_payment_ratio*100:.0f}% = {down_payment/10000:.2f} 万元
贷款金额: {loan_amount/10000:.2f} 万元
贷款年限: {years} 年 ({months} 个月)
贷款利率: {rate_percent:.2f}%

月供: {monthly_payment:.2f} 元
总还款: {total_payment/10000:.2f} 万元
总利息: {total_interest/10000:.2f} 万元
"""
        
        QMessageBox.information(None, "车贷计算结果", result)
        return result
    
    @staticmethod
    def income_tax_calculator():
        """个税计算器"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QDoubleSpinBox,
                                       QPushButton)
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("个税计算器（综合所得）")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 月度收入
        monthly_income = QDoubleSpinBox()
        monthly_income.setRange(0, 1000)
        monthly_income.setSuffix(" 元")
        monthly_income.setValue(10000)
        monthly_income.setSingleStep(1000)
        form.addRow("月度收入:", monthly_income)
        
        # 五险一金
        insurance = QDoubleSpinBox()
        insurance.setRange(0, 10000)
        insurance.setSuffix(" 元")
        insurance.setValue(2000)
        insurance.setSingleStep(500)
        form.addRow("五险一金:", insurance)
        
        # 专项附加扣除
        deductions = QDoubleSpinBox()
        deductions.setRange(0, 10000)
        deductions.setSuffix(" 元")
        deductions.setValue(1000)
        deductions.setSingleStep(500)
        form.addRow("专项附加扣除:", deductions)
        
        layout.addLayout(form)
        
        # 计算按钮
        calculate_btn = QPushButton("计算")
        calculate_btn.clicked.connect(lambda: CalculatorTools._calc_income_tax(
            monthly_income.value(),
            insurance.value(),
            deductions.value()
        ))
        layout.addWidget(calculate_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _calc_income_tax(monthly_income, insurance, deductions):
        """计算个税"""
        from PySide6.QtWidgets import QMessageBox
        
        # 累计预扣预缴应纳税所得额 = 累计收入 - 累计免税收入 - 累计减除费用 - 累计专项扣除 - 累计专项附加扣除
        # 减除费用 = 5000元/月
        
        annual_income = monthly_income * 12
        annual_insurance = insurance * 12
        annual_deductions = deductions * 12
        basic_deduction = 5000 * 12  # 基本减除费用
        
        taxable_income = annual_income - annual_insurance - annual_deductions - basic_deduction
        
        # 累进税率表（综合所得）
        tax_brackets = [
            (0, 36000, 0.03, 0),
            (36000, 144000, 0.10, 2520),
            (144000, 300000, 0.20, 16920),
            (300000, 420000, 0.25, 31920),
            (420000, 660000, 0.30, 52920),
            (660000, 960000, 0.35, 85920),
            (960000, float('inf'), 0.45, 181920),
        ]
        
        # 计算税额
        tax = 0
        for min_inc, max_inc, rate, deduction in tax_brackets:
            if taxable_income > min_inc:
                if taxable_income <= max_inc:
                    tax = taxable_income * rate - deduction
                    break
            else:
                break
        
        # 月度预扣税
        monthly_tax = tax / 12
        
        # 税后收入
        after_tax_income = monthly_income - insurance - monthly_tax
        
        result = f"""个税计算结果:
        
月度收入: {monthly_income:.2f} 元
年度收入: {annual_income:.2f} 元

五险一金: {insurance:.2f} 元/月 ({annual_insurance:.2f} 元/年)
专项附加扣除: {deductions:.2f} 元/月 ({annual_deductions:.2f} 元/年)
基本减除费用: 5000 元/月 (60000 元/年)

应纳税所得额: {max(0, taxable_income):.2f} 元/年
年度个税: {max(0, tax):.2f} 元
月度预扣税: {max(0, monthly_tax):.2f} 元

税后月收入: {after_tax_income:.2f} 元
"""
        
        QMessageBox.information(None, "个税计算结果", result)
        return result
    
    @staticmethod
    def base_conversion():
        """进制转换"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QLineEdit,
                                       QPushButton, QComboBox)
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("进制转换")
        dialog.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 输入数字
        input_number = QLineEdit()
        input_number.setPlaceholderText("请输入数字")
        form.addRow("输入:", input_number)
        
        # 选择输入进制
        input_base = QComboBox()
        input_base.addItems(["二进制", "八进制", "十进制", "十六进制"])
        input_base.setCurrentIndex(2)  # 默认十进制
        form.addRow("输入进制:", input_base)
        
        layout.addLayout(form)
        
        # 转换按钮
        convert_btn = QPushButton("转换")
        convert_btn.clicked.connect(lambda: CalculatorTools._convert_base(
            input_number.text(),
            input_base.currentIndex()
        ))
        layout.addWidget(convert_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _convert_base(number_str, input_base_idx):
        """进制转换"""
        from PySide6.QtWidgets import QMessageBox
        
        # 进制映射
        base_map = [2, 8, 10, 16]
        input_base = base_map[input_base_idx]
        
        try:
            # 转换为十进制
            if input_base == 2:
                decimal_value = int(number_str, 2)
            elif input_base == 8:
                decimal_value = int(number_str, 8)
            elif input_base == 10:
                decimal_value = int(number_str)
            else:  # 16
                decimal_value = int(number_str, 16)
            
            # 转换为其他进制
            binary = bin(decimal_value)[2:]
            octal = oct(decimal_value)[2:]
            hexadecimal = hex(decimal_value)[2:].upper()
            
            result = f"""进制转换结果:
            
十进制: {decimal_value}
二进制: {binary}
八进制: {octal}
十六进制: {hexadecimal}
"""
            
            QMessageBox.information(None, "转换结果", result)
            return result
        except ValueError:
            QMessageBox.warning(None, "错误", "输入的数字格式不正确")
            return None
    
    @staticmethod
    def date_countdown():
        """日期倒计时"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QPushButton,
                                       QDateEdit)
        from PySide6.QtCore import QDate
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("日期倒计时")
        dialog.setMinimumSize(400, 150)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 开始日期
        start_date = QDateEdit()
        start_date.setDate(QDate.currentDate())
        start_date.setCalendarPopup(True)
        form.addRow("开始日期:", start_date)
        
        # 结束日期
        end_date = QDateEdit()
        end_date.setDate(QDate.currentDate().addDays(100))  # 默认100天后
        end_date.setCalendarPopup(True)
        form.addRow("结束日期:", end_date)
        
        layout.addLayout(form)
        
        # 计算按钮
        calculate_btn = QPushButton("计算")
        calculate_btn.clicked.connect(lambda: CalculatorTools._calc_date_diff(
            start_date.date().toString("yyyy-MM-dd"),
            end_date.date().toString("yyyy-MM-dd")
        ))
        layout.addWidget(calculate_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _calc_date_diff(start_date_str, end_date_str):
        """计算日期差"""
        from PySide6.QtWidgets import QMessageBox
        from datetime import datetime
        
        try:
            start = datetime.strptime(start_date_str, "%Y-%m-%d")
            end = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            delta = end - start
            days = delta.days
            
            if days < 0:
                QMessageBox.warning(None, "错误", "结束日期必须晚于开始日期")
                return None
            
            weeks = days // 7
            remaining_days = days % 7
            
            years = days // 365
            months = days // 30
            
            result = f"""日期倒计时结果:
            
从 {start_date_str} 到 {end_date_str}

共计: {days} 天
约: {weeks} 周 {remaining_days} 天
约: {months} 个月
约: {years} 年
"""
            
            QMessageBox.information(None, "计算结果", result)
            return result
        except Exception as e:
            QMessageBox.warning(None, "错误", f"计算失败: {str(e)}")
            return None
    
    @staticmethod
    def age_calculator():
        """年龄天数计算"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QPushButton,
                                       QDateEdit)
        from PySide6.QtCore import QDate
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("年龄/天数计算")
        dialog.setMinimumSize(400, 150)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 出生日期
        birth_date = QDateEdit()
        birth_date.setDate(QDate(1990, 1, 1))  # 默认1990年
        birth_date.setCalendarPopup(True)
        form.addRow("出生日期:", birth_date)
        
        # 计算日期（默认今天）
        calc_date = QDateEdit()
        calc_date.setDate(QDate.currentDate())
        calc_date.setCalendarPopup(True)
        form.addRow("计算日期:", calc_date)
        
        layout.addLayout(form)
        
        # 计算按钮
        calculate_btn = QPushButton("计算")
        calculate_btn.clicked.connect(lambda: CalculatorTools._calc_age(
            birth_date.date().toString("yyyy-MM-dd"),
            calc_date.date().toString("yyyy-MM-dd")
        ))
        layout.addWidget(calculate_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _calc_age(birth_date_str, calc_date_str):
        """计算年龄"""
        from PySide6.QtWidgets import QMessageBox
        from datetime import datetime
        
        try:
            birth = datetime.strptime(birth_date_str, "%Y-%m-%d")
            calc = datetime.strptime(calc_date_str, "%Y-%m-%d")
            
            delta = calc - birth
            total_days = delta.days
            
            # 计算年龄（周岁）
            years = calc.year - birth.year
            if (calc.month, calc.day) < (birth.month, birth.day):
                years -= 1
            
            # 计算月份和天数
            months = calc.month - birth.month
            if calc.day < birth.day:
                months -= 1
            
            days = calc.day - birth.day
            if days < 0:
                # 借上个月的天数
                import calendar
                prev_month = calc.month - 1 if calc.month > 1 else 12
                prev_year = calc.year if calc.month > 1 else calc.year - 1
                days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
                days = days_in_prev_month + calc.day - birth.day
                months -= 1
            
            # 总周数
            weeks = total_days // 7
            
            # 总小时数、分钟数、秒数
            total_hours = total_days * 24
            total_minutes = total_hours * 60
            total_seconds = total_minutes * 60
            
            result = f"""年龄/天数计算结果:
            
出生日期: {birth_date_str}
计算日期: {calc_date_str}

年龄: {years} 岁 {months} 个月 {days} 天
共计: {total_days} 天
约: {weeks} 周
约: {total_days//30} 个月
约: {years} 岁

总小时数: {total_hours:,} 小时
总分钟数: {total_minutes:,} 分钟
总秒数: {total_seconds:,} 秒
"""
            
            QMessageBox.information(None, "计算结果", result)
            return result
        except Exception as e:
            QMessageBox.warning(None, "错误", f"计算失败: {str(e)}")
            return None
    
    @staticmethod
    def unit_conversion():
        """单位换算"""
        from PySide6.QtWidgets import (QInputDialog, QMessageBox, QDialog,
                                       QVBoxLayout, QFormLayout, QDoubleSpinBox,
                                       QPushButton, QComboBox)
        
        # 单位类型
        unit_types = ["长度", "重量", "体积", "网速"]
        
        # 创建对话框
        dialog = QDialog(None)
        dialog.setWindowTitle("单位换算")
        dialog.setMinimumSize(450, 250)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # 单位类型选择
        unit_type = QComboBox()
        unit_type.addItems(unit_types)
        form.addRow("单位类型:", unit_type)
        
        # 输入值
        input_value = QDoubleSpinBox()
        input_value.setRange(0, 999999999)
        input_value.setValue(1)
        input_value.setSingleStep(1)
        form.addRow("输入值:", input_value)
        
        # 源单位
        from_unit = QComboBox()
        form.addRow("从:", from_unit)
        
        # 目标单位
        to_unit = QComboBox()
        form.addRow("到:", to_unit)
        
        layout.addLayout(form)
        
        # 更新单位列表
        def update_units(index):
            from_unit.clear()
            to_unit.clear()
            
            if index == 0:  # 长度
                units = ["毫米", "厘米", "分米", "米", "千米", "英寸", "英尺", "码", "英里"]
            elif index == 1:  # 重量
                units = ["毫克", "克", "千克", "吨", "磅", "盎司"]
            elif index == 2:  # 体积
                units = ["毫升", "升", "立方米", "立方厘米", "加仑(美)", "加仑(英)"]
            else:  # 网速
                units = ["bps", "Kbps", "Mbps", "Gbps"]
            
            from_unit.addItems(units)
            to_unit.addItems(units)
            
            # 设置默认值
            if index == 0:  # 长度
                from_unit.setCurrentIndex(3)  # 米
                to_unit.setCurrentIndex(4)     # 千米
            elif index == 1:  # 重量
                from_unit.setCurrentIndex(2)  # 千克
                to_unit.setCurrentIndex(3)     # 吨
            elif index == 2:  # 体积
                from_unit.setCurrentIndex(1)  # 升
                to_unit.setCurrentIndex(0)     # 毫升
            else:  # 网速
                from_unit.setCurrentIndex(2)  # Mbps
                to_unit.setCurrentIndex(1)     # Kbps
        
        # 初始加载单位
        update_units(0)
        
        # 连接信号
        unit_type.currentIndexChanged.connect(update_units)
        
        # 转换按钮
        convert_btn = QPushButton("转换")
        convert_btn.clicked.connect(lambda: CalculatorTools._convert_unit(
            input_value.value(),
            unit_type.currentIndex(),
            from_unit.currentText(),
            to_unit.currentText()
        ))
        layout.addWidget(convert_btn)
        
        dialog.exec()
        
        return None
    
    @staticmethod
    def _convert_unit(value, unit_type_idx, from_unit, to_unit):
        """单位转换"""
        from PySide6.QtWidgets import QMessageBox
        
        # 定义转换因子（都先转换到基准单位，再转换到目标单位）
        if unit_type_idx == 0:  # 长度（基准：米）
            factors = {
                "毫米": 0.001,
                "厘米": 0.01,
                "分米": 0.1,
                "米": 1,
                "千米": 1000,
                "英寸": 0.0254,
                "英尺": 0.3048,
                "码": 0.9144,
                "英里": 1609.344
            }
        elif unit_type_idx == 1:  # 重量（基准：千克）
            factors = {
                "毫克": 0.000001,
                "克": 0.001,
                "千克": 1,
                "吨": 1000,
                "磅": 0.45359237,
                "盎司": 0.028349523
            }
        elif unit_type_idx == 2:  # 体积（基准：升）
            factors = {
                "毫升": 0.001,
                "升": 1,
                "立方米": 1000,
                "立方厘米": 0.001,
                "加仑(美)": 3.78541,
                "加仑(英)": 4.54609
            }
        else:  # 网速（基准：bps）
            factors = {
                "bps": 1,
                "Kbps": 1000,
                "Mbps": 1000000,
                "Gbps": 1000000000
            }
        
        try:
            # 转换到基准单位
            base_value = value * factors[from_unit]
            
            # 转换到目标单位
            result = base_value / factors[to_unit]
            
            unit_names = ["长度", "重量", "体积", "网速"]
            
            result_text = f"""{unit_names[unit_type_idx]}换算结果:
            
{value} {from_unit} = {result:.6g} {to_unit}
"""
            
            QMessageBox.information(None, "换算结果", result_text)
            return result_text
        except Exception as e:
            QMessageBox.warning(None, "错误", f"换算失败: {str(e)}")
            return None


if __name__ == "__main__":
    # 测试
    tools = CalculatorTools.get_tools()
    print(f"已加载 {len(tools)} 个计算器工具:")
    for tool in tools:
        print(f"  - {tool.icon} {tool.name}: {tool.description}")
