---
name: model-switch
description: 动态切换当前会话的模型 (Flash/Pro)，支持交互式菜单、智能搜索和标签。
metadata:
  openclaw:
    commands:
      - command: switch-model
        description: 🎭 打开模型选择菜单，支持按提供商分类、查看模型描述和标签。
---

# Model Switcher 🎭

利用 OpenClaw 的 Session Override 机制，在不修改 `openclaw.json` 的情况下动态切换当前会话使用的模型。
本技能优先读取 `agents.defaults.models` 中的官方目录，支持查看详细描述、标签，并支持按提供商过滤。

## 🎮 使用方法

1.  **交互式菜单**: 发送 `/switch-model` 或 “模型菜单”，我会列出所有可用模型供你选择（支持 Telegram 按钮）。
2.  **分类选择**: 菜单会先显示提供商列表（如 Google, OpenAI），点击后再显示具体模型。
3.  **模糊搜索**: “切换到代码模型”、“换个写代码厉害的”、“用 flash 模型” 或 “重置模型”。

## 🤖 模型映射 (Aliases)

- **flash**: `google/gemini-3-flash-preview` (速度快，便宜，适合简单任务)
- **pro**: `google/gemini-3-pro-preview` (聪明，适合复杂任务)
- **default**: `default` (清除覆盖，使用系统默认)

## 🛠️ 脚本工具

**获取可用模型列表或查找特定模型：**

```bash
# 获取模型提供商列表 (用于顶级菜单)
python3 skills/model-switch/scripts/list_models.py

# 获取特定提供商的模型列表 (用于次级菜单)
python3 skills/model-switch/scripts/list_models.py <provider_name>

# 智能搜索 (匹配 ID, Alias, Tags 或提供商)
python3 skills/model-switch/scripts/list_models.py <keyword>
```

## ⚙️ 执行逻辑 (Agent SOP)

### 场景 1: 顶级菜单 - 列出提供商 (`/switch-model`)
**触发条件**: 命令参数为空。
1.  **调用脚本**: `python3 skills/model-switch/scripts/list_models.py` (不带参数)。
2.  **构建菜单**:
    *   为返回的每个 Provider 创建一个按钮。
    *   **Callback Data**: `/switch-model provider:<name>` (例如 `/switch-model provider:google`)。
    *   **发送菜单**: "请选择模型提供商："

### 场景 2: 次级菜单 - 列出具体模型 (`/switch-model provider:<name>`)
**触发条件**: 参数包含 `provider:`。
1.  **调用脚本**: `python3 skills/model-switch/scripts/list_models.py <name>` (提取冒号后内容)。
2.  **构建菜单**:
    *   遍历返回的 JSON 列表。
    *   **按钮文本**: 优先显示 `alias` 或 `short_id`。
    *   **Callback Data**: `/switch-model <full_id>`。
    *   **发送文本**: 包含模型 `description` 和 `tags`（如有）。

### 场景 3: 模糊搜索与直接切换
1.  **执行逻辑**: 调用脚本搜索关键词。
2.  **单一结果**: 直接执行 `session_status(model=full_id)`。
3.  **多个结果**: 显示匹配的模型列表按钮供用户选择。

## 💻 Telegram 菜单示例

```json
{
  "action": "send",
  "message": "请选择模型提供商：",
  "buttons": [
    [ { "text": "Google", "callback_data": "/switch-model provider:google" } ],
    [ { "text": "OpenAI", "callback_data": "/switch-model provider:openai" } ],
    [ { "text": "🔄 重置为默认", "callback_data": "/switch-model default" } ]
  ]
}
```
