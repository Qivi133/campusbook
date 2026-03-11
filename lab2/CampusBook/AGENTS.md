# AGENTS.md - CampusBook 项目规则

## 项目概述

CampusBook 是一个面向大学生的二手书交易平台，采用 Flask + SQLite 技术栈开发。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Flask 3.0 (Python) |
| 数据库 | SQLite + SQLAlchemy |
| 认证 | Flask-Login |
| 前端 | HTML + CSS + JavaScript (原生) |
| 模板 | Jinja2 |

---

## 功能范围 (V1.0)

### 核心功能 (必须实现)

| 模块 | 功能 |
|------|------|
| 用户系统 | 注册、登录、登出 |
| 书籍系统 | 发布、浏览、详情、编辑、删除 |
| 搜索系统 | 关键词搜索、分类筛选 |
| 交易系统 | 购物车、下单、订单查看 |

### 禁止添加 (V1.0阶段)

以下功能在 V1.0 阶段 **禁止实现**，保持项目简洁：
- 用户评价系统
- 消息通知提醒
- 收藏功能
- 管理员后台
- 在线支付
- 社交分享
- 高级排序（除默认外）

---

## 代码规范

### Python (app.py)

- 使用 SQLAlchemy ORM 操作数据库
- 密码使用 Werkzeug `generate_password_hash` 存储
- 所有路由必须添加 `@login_required` 装饰器（除公开页面）
- 表单提交使用 POST 方法
- 错误提示使用 `flash()` 消息

### 前端 (templates/)

- 使用 Jinja2 模板引擎
- 继承 `base.html` 基础模板
- 响应式设计，支持移动端
- CSS 样式统一在 `static/style.css`

### 文件结构

```
CampusBook/
├── app.py                 # 主应用（所有路由和模型）
├── requirements.txt       # 依赖列表
├── start.bat             # 启动脚本
├── SPEC.md               # 概要规范
├── 需求文档V1.0.md       # V1.0需求
├── static/
│   ├── style.css         # 样式文件
│   └── uploads/          # 图片上传目录
└── templates/             # Jinja2模板
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── book_detail.html
    ├── new_book.html
    ├── edit_book.html
    ├── cart.html
    ├── orders.html
    ├── messages.html
    ├── profile.html
    └── my_books.html
```

---

## 数据库模型

### User
| 字段 | 类型 |
|------|------|
| id | Integer (PK) |
| username | String(50) - Unique |
| email | String(100) - Unique |
| password_hash | String(200) |
| phone | String(20) |
| created_at | DateTime |

### Book
| 字段 | 类型 |
|------|------|
| id | Integer (PK) |
| title | String(200) |
| author | String(100) |
| isbn | String(20) |
| category | String(50) |
| price | Float |
| description | Text |
| image_url | String(200) |
| condition | String(20) |
| seller_id | Integer (FK) |
| status | String(20) - available/sold |
| created_at | DateTime |

### Order
| 字段 | 类型 |
|------|------|
| id | Integer (PK) |
| buyer_id | Integer (FK) |
| book_id | Integer (FK) |
| total_price | Float |
| status | String(20) |
| contact_message | String(500) |
| created_at | DateTime |

### CartItem
| 字段 | 类型 |
|------|------|
| id | Integer (PK) |
| user_id | Integer (FK) |
| book_id | Integer (FK) |
| created_at | DateTime |

### Message
| 字段 | 类型 |
|------|------|
| id | Integer (PK) |
| sender_id | Integer (FK) |
| receiver_id | Integer (FK) |
| content | String(500) |
| book_id | Integer (FK) |
| created_at | DateTime |
| is_read | Boolean |

---

## 开发规则

### 新增功能

1. 先在 `需求文档V1.0.md` 中确认功能在范围内
2. 在 `app.py` 中添加路由和数据模型（如需要）
3. 在 `templates/` 中创建或复用模板
4. 更新 `static/style.css`（如需要新样式）

### 路由命名规范

| 功能 | 路由风格 |
|------|----------|
| 列表 | GET /items |
| 详情 | GET /item/<id> |
| 创建 | GET/POST /item/new |
| 编辑 | GET/POST /item/<id>/edit |
| 删除 | POST /item/<id>/delete |
| 操作 | POST /action/<id> |

### 安全要求

- 密码必须哈希存储
- 用户输入必须验证
- SQL 使用 ORM 防止注入
- XSS 由 Jinja2 自动转义
- 敏感操作需要登录验证

---

## 启动命令

```bash
cd c:\Users\Qivii\AI_lab\lab2\CampusBook
pip install Flask Flask-SQLAlchemy Flask-Login
python app.py
```

访问地址：`http://127.0.0.1:5000`

---

## 注意事项

- V1.0 阶段保持功能简洁，聚焦核心交易流程
- 不添加不必要的依赖
- 不创建额外的配置文件
- 所有代码放在 `app.py` 中（单文件原则）
