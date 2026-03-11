# CampusBook 二手书交易平台规范

## 1. 项目概述

- **项目名称**: CampusBook
- **项目类型**: 校园二手书交易 Web 应用
- **核心功能**: 为大学生提供二手书买卖、交换的平台
- **目标用户**: 大学生群体

## 2. 技术栈

- **后端**: Flask (Python)
- **数据库**: SQLite + SQLAlchemy
- **前端**: HTML + CSS + JavaScript (原生)
- **认证**: Flask-Login

## 3. 功能规范

### 3.1 用户系统
- 用户注册 (用户名、邮箱、密码)
- 用户登录/登出
- 个人资料管理
- 查看我的订单/出售记录

### 3.2 书籍系统
- 发布书籍 (标题、作者、ISBN、分类、价格、描述、图片)
- 浏览所有书籍
- 书籍详情页
- 编辑/删除自己发布的书籍
- 书籍分类 (教材、文学、专业课、考研、公务员、其他)

### 3.3 搜索系统
- 按关键词搜索书名/作者
- 按分类筛选
- 价格区间筛选
- 排序 (最新发布、价格从低到高、价格从高到低)

### 3.4 交易系统
- 加入购物车
- 下单购买
- 订单管理 (待付款、待发货、已完成、已取消)
- 确认收货

### 3.5 消息系统
- 买家联系卖家

## 4. 数据库模型

### User (用户)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String(50) | 用户名 (唯一) |
| email | String(100) | 邮箱 (唯一) |
| password_hash | String(200) | 密码哈希 |
| phone | String(20) | 电话 |
| created_at | DateTime | 创建时间 |

### Book (书籍)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| title | String(200) | 书名 |
| author | String(100) | 作者 |
| isbn | String(20) | ISBN |
| category | String(50) | 分类 |
| price | Float | 价格 |
| description | Text | 描述 |
| image_url | String(200) | 图片URL |
| condition | String(20) | 新旧程度 |
| seller_id | Integer | 卖家ID |
| status | String(20) | 状态 (available/sold) |
| created_at | DateTime | 发布时间 |

### Order (订单)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| buyer_id | Integer | 买家ID |
| book_id | Integer | 书籍ID |
| total_price | Float | 总价 |
| status | String(20) | 状态 |
| created_at | DateTime | 创建时间 |
| contact_message | String(500) | 留言 |

### CartItem (购物车)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户ID |
| book_id | Integer | 书籍ID |
| created_at | DateTime | 添加时间 |

### Message (消息)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| sender_id | Integer | 发送者ID |
| receiver_id | Integer | 接收者ID |
| content | String(500) | 内容 |
| book_id | Integer | 相关书籍ID |
| created_at | DateTime | 发送时间 |
| is_read | Boolean | 已读状态 |

## 5. 页面结构

### 前端页面
1. **首页** (`/`) - 展示所有在售书籍，搜索筛选
2. **登录页** (`/login`)
3. **注册页** (`/register`)
4. **书籍详情页** (`/book/<id>`)
5. **发布书籍页** (`/book/new`)
6. **编辑书籍页** (`/book/<id>/edit`)
7. **购物车页** (`/cart`)
8. **订单页** (`/orders`)
9. **个人中心** (`/profile`)
10. **消息中心** (`/messages`)

## 6. 验收标准

- [ ] 用户可以注册、登录、登出
- [ ] 用户可以发布二手书信息
- [ ] 用户可以浏览和搜索书籍
- [ ] 用户可以将书籍加入购物车
- [ ] 用户可以下单购买
- [ ] 用户可以管理自己的订单
- [ ] 用户可以互相发送消息
- [ ] 页面美观、响应式设计
- [ ] 无安全漏洞 (SQL注入、XSS等)
