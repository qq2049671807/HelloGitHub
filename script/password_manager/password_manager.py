import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLabel, QLineEdit, QTextEdit, QMessageBox,
                             QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from database import DatabaseManager


class AddEditDialog(QDialog):
    def __init__(self, parent=None, account_data=None):
        super().__init__(parent)
        self.account_data = account_data
        self.is_edit_mode = account_data is not None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('编辑账号' if self.is_edit_mode else '添加账号')
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        self.website_label = QLabel('网站/应用名称:')
        self.website_input = QLineEdit()
        if self.account_data:
            self.website_input.setText(self.account_data['website'])
        
        self.username_label = QLabel('用户名/账号:')
        self.username_input = QLineEdit()
        if self.account_data:
            self.username_input.setText(self.account_data['username'])
        
        self.password_label = QLabel('密码:')
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        if self.account_data:
            self.password_input.setText(self.account_data['password'])
        
        self.show_password_btn = QPushButton('显示')
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_btn)
        
        self.notes_label = QLabel('备注:')
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        if self.account_data:
            self.notes_input.setPlainText(self.account_data['notes'] or '')
        
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton('保存')
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(self.website_label)
        layout.addWidget(self.website_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addLayout(password_layout)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_input)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def toggle_password_visibility(self):
        if self.show_password_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText('隐藏')
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText('显示')
    
    def get_data(self):
        return {
            'website': self.website_input.text().strip(),
            'username': self.username_input.text().strip(),
            'password': self.password_input.text(),
            'notes': self.notes_input.toPlainText().strip()
        }
    
    def accept(self):
        data = self.get_data()
        if not data['website']:
            QMessageBox.warning(self, '警告', '请输入网站/应用名称！')
            return
        if not data['username']:
            QMessageBox.warning(self, '警告', '请输入用户名/账号！')
            return
        if not data['password']:
            QMessageBox.warning(self, '警告', '请输入密码！')
            return
        super().accept()


class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.load_accounts()
    
    def init_ui(self):
        self.setWindowTitle('密码管理器')
        self.setGeometry(100, 100, 900, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        toolbar_layout = QHBoxLayout()
        self.add_btn = QPushButton('添加账号')
        self.add_btn.clicked.connect(self.add_account)
        
        self.edit_btn = QPushButton('编辑')
        self.edit_btn.clicked.connect(self.edit_account)
        
        self.delete_btn = QPushButton('删除')
        self.delete_btn.clicked.connect(self.delete_account)
        
        self.copy_password_btn = QPushButton('复制密码')
        self.copy_password_btn.clicked.connect(self.copy_password)
        
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.copy_password_btn)
        toolbar_layout.addStretch()
        
        search_layout = QHBoxLayout()
        self.search_label = QLabel('搜索:')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('输入网站名或账号进行搜索...')
        self.search_input.textChanged.connect(self.search_accounts)
        self.clear_search_btn = QPushButton('清除')
        self.clear_search_btn.clicked.connect(self.clear_search)
        
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.clear_search_btn)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', '网站/应用', '账号', '密码', '备注'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        self.table.doubleClicked.connect(self.edit_account)
        
        main_layout.addLayout(toolbar_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)
        
        central_widget.setLayout(main_layout)
    
    def load_accounts(self, accounts=None):
        if accounts is None:
            accounts = self.db.get_all_accounts()
        
        self.table.setRowCount(len(accounts))
        
        for row, account in enumerate(accounts):
            self.table.setItem(row, 0, QTableWidgetItem(str(account['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(account['website']))
            self.table.setItem(row, 2, QTableWidgetItem(account['username']))
            
            password_display = '*' * min(len(account['password']), 12)
            password_item = QTableWidgetItem(password_display)
            password_item.setData(Qt.UserRole, account['password'])
            self.table.setItem(row, 3, password_item)
            
            notes_preview = account['notes'][:50] + '...' if account['notes'] and len(account['notes']) > 50 else account['notes']
            self.table.setItem(row, 4, QTableWidgetItem(notes_preview or ''))
    
    def add_account(self):
        dialog = AddEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.db.add_account(
                    data['website'],
                    data['username'],
                    data['password'],
                    data['notes']
                )
                QMessageBox.information(self, '成功', '账号添加成功！')
                self.load_accounts()
            except Exception as e:
                QMessageBox.critical(self, '错误', f'添加账号失败：{str(e)}')
    
    def edit_account(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要编辑的账号！')
            return
        
        account_id = int(self.table.item(selected_row, 0).text())
        account_data = self.db.get_account_by_id(account_id)
        
        if not account_data:
            QMessageBox.critical(self, '错误', '无法获取账号信息！')
            return
        
        dialog = AddEditDialog(self, account_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.db.update_account(
                    account_id,
                    data['website'],
                    data['username'],
                    data['password'],
                    data['notes']
                )
                QMessageBox.information(self, '成功', '账号更新成功！')
                self.load_accounts()
            except Exception as e:
                QMessageBox.critical(self, '错误', f'更新账号失败：{str(e)}')
    
    def delete_account(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的账号！')
            return
        
        account_id = int(self.table.item(selected_row, 0).text())
        website = self.table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'确定要删除账号 "{website}" 吗？\n此操作无法撤销！',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_account(account_id)
                QMessageBox.information(self, '成功', '账号删除成功！')
                self.load_accounts()
            except Exception as e:
                QMessageBox.critical(self, '错误', f'删除账号失败：{str(e)}')
    
    def copy_password(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要复制密码的账号！')
            return
        
        password_item = self.table.item(selected_row, 3)
        password = password_item.data(Qt.UserRole)
        
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        QMessageBox.information(self, '成功', '密码已复制到剪贴板！')
    
    def search_accounts(self):
        keyword = self.search_input.text().strip()
        if keyword:
            accounts = self.db.search_accounts(keyword)
            self.load_accounts(accounts)
        else:
            self.load_accounts()
    
    def clear_search(self):
        self.search_input.clear()
        self.load_accounts()


def main():
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
