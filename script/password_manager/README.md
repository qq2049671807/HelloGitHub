# 密码管理器

一个基于 PyQt5 的桌面应用程序，用于安全地管理您的账号密码信息。

## 功能特性

### 核心功能
- ✅ **添加账号**: 存储网站/应用名称、用户名、密码和备注信息
- ✅ **查看账号**: 以表格形式展示所有账号信息
- ✅ **编辑账号**: 修改现有账号的任何信息
- ✅ **删除账号**: 安全删除账号（带确认提示）
- ✅ **搜索功能**: 根据网站名或账号快速搜索
- ✅ **复制密码**: 一键复制密码到剪贴板

### 安全特性
- 🔐 密码使用 Fernet 加密算法存储
- 👁️ 密码字段默认隐藏显示（***）
- 🔄 可切换密码显示/隐藏
- 💾 本地 SQLite 数据库存储

## 技术栈

- **Python 3.7+**
- **PyQt5**: GUI 框架
- **SQLite**: 本地数据存储
- **cryptography**: 密码加密

## 安装说明

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

#### Windows 用户
双击运行 `run.bat` 文件，或在命令行中执行：
```cmd
python password_manager.py
```

#### Linux/Mac 用户
在终端中执行：
```bash
./run.sh
# 或者
python3 password_manager.py
```

## 使用指南

### 添加新账号
1. 点击 "添加账号" 按钮
2. 填写网站/应用名称、用户名、密码和备注（可选）
3. 点击 "保存"

### 编辑账号
1. 在表格中选择要编辑的账号
2. 点击 "编辑" 按钮或双击该行
3. 修改信息后点击 "保存"

### 删除账号
1. 在表格中选择要删除的账号
2. 点击 "删除" 按钮
3. 确认删除操作

### 复制密码
1. 在表格中选择账号
2. 点击 "复制密码" 按钮
3. 密码已复制到剪贴板

### 搜索账号
1. 在搜索框中输入网站名或账号关键词
2. 表格会自动筛选匹配的结果
3. 点击 "清除" 按钮恢复完整列表

## 文件说明

```
password_manager/
├── password_manager.py   # 主程序，包含 PyQt5 GUI 界面
├── database.py          # 数据库操作模块
├── crypto_utils.py      # 加密/解密工具模块
├── requirements.txt     # Python 依赖包列表
├── README.md           # 说明文档
├── passwords.db        # SQLite 数据库文件（运行后自动生成）
└── secret.key          # 加密密钥文件（运行后自动生成）
```

## 安全注意事项

⚠️ **重要提醒**：

1. **密钥文件保护**: `secret.key` 文件包含加密密钥，丢失此文件将无法解密已存储的密码。请妥善备份并保管此文件。

2. **数据库备份**: 建议定期备份 `passwords.db` 文件。

3. **本地存储**: 所有数据存储在本地，不会上传到云端。

4. **密钥管理**: 不要将 `secret.key` 和 `passwords.db` 文件上传到公共仓库或分享给他人。

## 数据库结构

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,  -- 加密存储
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

## 常见问题

**Q: 忘记了某个账号的密码怎么办？**  
A: 本程序只是存储和管理您的密码，如果您忘记了某个账号的实际密码，需要通过该网站/应用的密码重置功能找回。

**Q: 可以在多台电脑上使用吗？**  
A: 可以，但需要同时复制 `passwords.db` 和 `secret.key` 文件到其他电脑。

**Q: 数据安全吗？**  
A: 密码使用 Fernet 对称加密算法加密存储，只要保护好 `secret.key` 文件，数据是安全的。

## 系统要求

- Windows 7 及以上版本
- Python 3.7 或更高版本
- 至少 50MB 可用磁盘空间

## 许可证

本项目仅供学习和个人使用。

## 开发者

如需扩展功能或报告问题，请联系开发团队。

---

**提示**: 首次运行时，程序会自动创建数据库和加密密钥文件。
