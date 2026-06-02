# 📚 智学编程

一个基于 Streamlit 的智能编程学习平台，支持多语言编程练习、AI 辅助学习和个性化讲解。

## ✨ 主要功能

### 📖 学习中心
- 思维导图式知识点学习
- 支持 Python / C++ / C / Java 四种语言
- 8 大技术分类，50+ 知识点详解
- 代码示例 + 核心概念 + 动手实践

### 💻 练习中心
- 随机题库挑战
- 难度筛选（基础/中等/进阶）
- 实时代码测试
- 成绩统计和掌握度分析

### 📊 学习报告
- 知识点掌握度可视化
- 题库统计概览
- 练习进度追踪
- 数据和图表展示

### 🤖 AI 编程助手
**1. 生成练习题**
- AI 自动生成匹配的编程题目
- 智能难度控制
- 完整的测试用例和参考答案
- 一键加入自定义题库

**2. 知识问答**
- 24/7 在线编程问题解答
- 支持算法、数据结构、语法等多方面
- 对话式学习体验

**3. 代码复盘**
- AI 深度分析代码逻辑
- 时间/空间复杂度分析
- 优化建议和分步讲解

**4. 自定义题库**
- 个性化题目管理
- 独立练习和测试
- 掌握度追踪

### 📖 个性化讲解
- 精选知识点讲解
- 代码逐行解析
- 配套练习题

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 启动

## 📦 项目结构

```
智学编程/
├── app.py              # 主应用文件（主逻辑）
├── requirements.txt    # Python 依赖包
├── README.md          # 项目说明文档
├── 设计文档.md        # 详细设计文档
├── demo.py           # 示例代码
└── app_backup.py     # 备份文件（可选）
```

## 🛠️ 技术栈

- **前端框架**: Streamlit
- **语言**: Python 3.8+
- **代码编辑器**: Monaco Editor (VS Code 同款)
- **AI 助手**: 支持 OpenAI API（GPT-3.5/4）
- **代码执行**: 本地 Python 解释器

## 🔧 API 配置

AI 功能需要配置 API Key：

```python
# 在申请页面（需要根据你的需求修改位置）
api_key = st.text_input("API Key", type="password", 
                      value="", 
                      key="api_key_input")
api_endpoint = st.text_input("API 地址", 
                        placeholder="https://api.openai.com/v1/chat/completions",
                        value="https://chat.ecnu.edu.cn/open/api/v1/chat/completions",
                        key="api_endpoint_input")
```

### 支持的 API
- OpenAI 官方 API
- 华东师大 Chat API（默认）
- 其他兼容 OpenAI API 的服务

## 🎯 支持的语言

| 语言 | 特性 |
|------|------|
| **Python** | 完整支持，优先推荐 |
| **C++** | 完整支持 |
| **C** | 基础功能 |
| **Java** | 完整支持 |

## 📚 知识体系

### 语言基础
- Hello World
- 变量与数据类型
- 输入输出
- 条件判断与循环

### 数据结构
- 数组与字符串
- 链表
- 栈与队列
- 树与图

### 算法
- 递归与分治
- 动态规划
- 贪心算法
- 回溯算法
- 二分查找
- 排序算法

## 🔐 隐私说明

- API Key 本地存储，不传输到其他服务器
- 测试数据仅在本地运行
- 代码执行在本地 Python 环境

## 📝 使用说明

### 新手入门
1. **学习知识** → 学习中心查看概念
2. **打开 AI助手** → 生成练习题
3. **写代码** → 在代码编辑器中编写
4. **提交测试** → 查看结果和答案
5. **加入题库** → 喜欢的题目收藏起来

### 进阶学习
1. **专项练习** → 选择知识点集中训练
2. **随机挑战** → 每日一练
3. **代码复盘** → AI 帮你分析代码
4. **知识问答** → 随时提问

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 如何贡献
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证

## 🎉 致谢

- [Streamlit](https://streamlit.io/) - Web 应用框架
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - 代码编辑器
- OpenAI API - AI 辅助功能
- [常见算法题库](https://leetcode.com/) - 参考部分题目

## 📧 联系方式

如有问题或建议，欢迎通过 Issue 联系

---

⭐ **如果这个项目对你有帮助，请给个 Star！**
