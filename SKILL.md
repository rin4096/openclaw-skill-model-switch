---
name: model-switch
description: 动态切换当前会话的模型 (Flash/Pro)，无需修改配置文件。支持交互式菜单。
---

# Model Switcher 🎭

利用 OpenClaw 的 Session Override 机制，在不修改 `openclaw.json` 的情况下动态切换当前会话使用的模型。
本技能包含一个脚本，可实时读取 `openclaw.json` 中的模型列表，自动识别 Flash/Pro 模型。

## 🎮 使用方法

1.  **交互式菜单**: 发送 `/switch-model` 或 “模型菜单”，我会列出所有可用模型供你选择（支持 Telegram 按钮）。
2.  **直接命令**: “切换模型到 flash”、“用 pro 模型” 或 “重置模型”。

## 🤖 模型映射 (Aliases)

- **flash**: `google/gemini-3-flash-preview` (速度快，便宜，适合简单任务)
- **pro**: `google/gemini-3-pro-preview` (聪明，适合复杂任务)
- **default**: `default` (清除覆盖，使用系统默认)

**注意**: 技能脚本支持模糊搜索，你可以尝试搜索任何模型关键词（如 `claude`, `gpt`, `openai` 等）。

## 🛠️ 脚本工具

**获取可用模型列表或查找特定模型：**

```bash
# 列出所有模型 (返回 JSON 列表)
python3 skills/model-switch/scripts/list_models.py

# 查找特定模型 (支持模糊匹配)
python3 skills/model-switch/scripts/list_models.py <keyword>
```

## ⚙️ 执行逻辑 (Agent SOP)

### 场景 1: 用户请求菜单 (`/switch-model`)
1.  **调用脚本**: 运行 `python3 skills/model-switch/scripts/list_models.py` 获取 JSON 列表。
2.  **构建菜单**:
    *   **Telegram**: 使用 `message` 工具发送带 `buttons` 的消息。
        *   按钮格式: `text="Alias/ID"`, `callback_data="/switch-model <Full_ID>"`。
        *   记得加一个 "Reset Default" 按钮。
    *   **其他平台**: 发送文本列表，让用户回复序号或 ID。

### 场景 2: 用户执行切换 (`/switch-model <ID>` 或 点击按钮)
1.  **解析 ID**: 获取用户提供的 `<Full_ID>` (例如 `google/gemini-3-flash-preview`)。
2.  **执行切换**: 调用 `session_status(model="<Full_ID>")`。
3.  **反馈**: 告知用户已切换，并显示当前模型信息。

### 场景 3: 模糊搜索切换 ("切换到 claude")
1.  **调用脚本查找**: 运行 `python3 skills/model-switch/scripts/list_models.py <keyword>`。
2.  **处理输出**:
    *   **单一结果**: 直接切换。
    *   **多项结果**: 列出选项让用户选。
    *   **无结果**: 报错。

## 💻 示例：发送 Telegram 菜单

```json
// 调用 message 工具
{
  "action": "send",
  "message": "请选择要切换的模型：",
  "buttons": [
    [
      { "text": "⚡️ Flash", "callback_data": "/switch-model google/gemini-3-flash-preview" },
      { "text": "🧠 Pro", "callback_data": "/switch-model google/gemini-3-pro-preview" }
    ],
    [
      { "text": "🔄 Reset Default", "callback_data": "/switch-model default" }
    ]
  ]
}
```
