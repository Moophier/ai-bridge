# AI算力匹配桥 (AIBridge)

> AI算力匹配桥 - 连接闲置GPU与AI推理需求

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/ai-bridge)](https://github.com/yourusername/ai-bridge/stargazers)
[![License](https://img.shields.io/github/license/yourusername/ai-bridge)](https://github.com/yourusername/ai-bridge/blob/main/LICENSE)

## 项目简介

AIBridge 是一个AI算力匹配平台，连接有GPU资源的提供者和需要AI推理能力的用户。

**当前阶段**: MVP (原型)

## 功能特性

- 用户提交AI推理任务
- 支持多种开源模型 (Llama 3, Mistral, Qwen)
- Redis异步任务队列
- 实时任务状态追踪
- Docker一键部署

## 技术栈

### 后端
- FastAPI - API框架
- Redis + RQ - 任务队列
- SQLAlchemy - ORM
- SQLite/PostgreSQL - 数据库

### 前端
- Next.js 14 - React框架
- Tailwind CSS - UI样式

## 快速开始

### 本地开发

```bash
# 克隆项目
git clone https://github.com/yourusername/ai-bridge.git
cd ai-bridge

# 启动后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 启动前端 (新终端)
cd frontend
npm install
npm run dev

# 启动Worker (新终端)
rq worker ai-tasks
```

### Docker部署

```bash
docker-compose up --build
```

访问:
- 前端: http://localhost:3000
- API文档: http://localhost:8000/docs

## API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/submit` | POST | 提交推理任务 |
| `/result/{task_id}` | GET | 获取任务结果 |
| `/tasks` | GET | 任务列表 |
| `/models` | GET | 可用模型 |

## 项目路线图

| 阶段 | 时间 | 目标 |
|------|------|------|
| MVP | 1-3月 | 基础API + 前端 |
| Alpha | 4-6月 | 接入真实GPU |
| Beta | 7-12月 | Token经济 |
| 1.0 | 1年+ | 去中心化网络 |

## 许可证

MIT License - see [LICENSE](LICENSE)

## 贡献

欢迎提交Issue和Pull Request!
