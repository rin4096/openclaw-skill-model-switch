---
name: model-switcher
description: Interactive menu to list and switch between available AI models in OpenClaw. Use when the user wants to change the current model, see available models, or switch to a different LLM provider. Trigger on phrases like "switch model", "change model", "list models", "use gemini/gpt/kimi", or when the user asks what models are available.
metadata:
  {
    "openclaw":
    {
      "emoji": "🔄",
      "requires": { "bins": ["bash", "jq"] }
    }
  }
---

# Model Switcher

純文字選單，用於切換 OpenClaw 的 AI 模型。

## 使用流程

1. 執行腳本顯示選單：`bash {baseDir}/scripts/model-switcher.sh`
2. 將輸出原樣發給用戶
3. 用戶回覆編號後，執行切換

## 切換操作

| 用戶輸入 | 操作 |
|---------|------|
| `1`-`N` | `session_status model=<對應的 model_id>` |
| `0` | `session_status model=default` |
| 模型別名（如 `gemini`） | `session_status model=<別名>` |

## 錯誤處理

- 用戶輸入超出範圍 → 提示有效範圍（0-N）
- 用戶輸入非數字 → 嘗試匹配模型名稱或別名，找不到則提示重新選擇

## 注意事項

- **純文字選單**，不使用 inline buttons
- 腳本標記的是配置中的默認模型（`model.primary`），不是 session 級別的覆蓋
- Session 級別的覆蓋由 `session_status` 管理，腳本不感知

## 結構

```
skills/model-switcher/
├── SKILL.md
└── scripts/
    └── model-switcher.sh
```
