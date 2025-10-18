# 密码管理器 - 功能清单

## ✅ 已实现的功能

### 1. 用户界面（PyQt5）
- [x] 主窗口设计，包含账号列表展示区域
- [x] 添加账号按钮和对话框（网站/应用名称、账号、密码、备注）
- [x] 编辑和删除功能按钮
- [x] 搜索/筛选功能
- [x] 清晰的中文界面

### 2. 数据管理
- [x] 使用 SQLite 数据库存储账号信息
- [x] 密码加密存储（使用 cryptography 库的 Fernet 加密）
- [x] 支持添加账号记录
- [x] 支持查看账号记录
- [x] 支持编辑账号记录
- [x] 支持删除账号记录

### 3. 安全特性
- [x] 密码字段显示时使用遮罩（***）
- [x] 提供"显示密码"按钮切换可见性
- [x] 密码复制到剪贴板功能
- [x] 加密密钥自动生成和管理

### 4. 基础功能列表
- [x] 添加新账号记录（网站名、用户名、密码、备注）
- [x] 查看账号列表（表格视图）
- [x] 编辑现有记录
- [x] 删除记录（带确认提示）
- [x] 搜索功能（按网站名或账号搜索）
- [x] 复制密码到剪贴板

## 📁 文件结构

```
script/password_manager/
├── password_manager.py       # 主程序，包含 PyQt5 GUI
├── database.py              # 数据库操作模块
├── crypto_utils.py          # 加密工具模块
├── requirements.txt         # 依赖列表
├── README.md               # 使用说明文档
├── FEATURES.md             # 功能清单（本文件）
├── run.sh                  # Linux/Mac 启动脚本
├── run.bat                 # Windows 启动脚本
├── verify_installation.py  # 安装验证脚本
├── test_basic.py           # 基础功能测试脚本
└── __init__.py             # Python 包初始化文件
```

## 🔧 技术实现细节

### 加密模块 (crypto_utils.py)
- **CryptoManager 类**
  - 自动生成或加载加密密钥
  - 提供 encrypt() 和 decrypt() 方法
  - 使用 Fernet 对称加密算法

### 数据库模块 (database.py)
- **DatabaseManager 类**
  - 自动初始化 SQLite 数据库
  - 表结构：id, website, username, password, notes, created_at, updated_at
  - 提供 CRUD 操作方法：
    - add_account()
    - get_all_accounts()
    - get_account_by_id()
    - update_account()
    - delete_account()
    - search_accounts()

### GUI 模块 (password_manager.py)
- **PasswordManager 类**（主窗口）
  - QTableWidget 显示账号列表
  - 工具栏按钮：添加、编辑、删除、复制密码
  - 搜索栏实时筛选
  - 双击表格行快速编辑

- **AddEditDialog 类**（添加/编辑对话框）
  - 输入字段：网站、用户名、密码、备注
  - 密码显示/隐藏切换
  - 输入验证

## 🔒 安全考虑

1. **密码加密**
   - 使用 Fernet 对称加密
   - 密钥存储在 secret.key 文件
   - 数据库中只存储加密后的密码

2. **本地存储**
   - 所有数据存储在本地 SQLite 数据库
   - 不涉及网络传输
   - 密钥文件与数据库分离

3. **界面安全**
   - 密码默认以星号显示
   - 需要手动点击才能显示明文密码
   - 删除操作需要确认

## 🎯 使用场景

- 个人密码管理
- 团队账号管理（本地使用）
- 测试账号管理
- 开发环境账号管理

## 📊 性能特性

- 轻量级应用，内存占用小
- SQLite 数据库，无需额外服务
- 即时搜索和筛选
- 加密解密性能优异

## 🚀 未来可能的扩展功能

- 密码强度检查
- 密码生成器
- 多用户支持（主密码保护）
- 数据导入/导出功能
- 密码过期提醒
- 标签分类功能
- 备份和恢复功能
- 云端同步（可选）

## 📝 注意事项

1. ⚠️ **密钥文件保护**：`secret.key` 文件非常重要，丢失将无法解密密码
2. 📦 **数据备份**：建议定期备份 `passwords.db` 和 `secret.key`
3. 🔐 **密钥保密**：不要将密钥文件上传到公共仓库
4. 💻 **系统要求**：Python 3.7+, PyQt5, cryptography

---

最后更新日期：2024-10-18
