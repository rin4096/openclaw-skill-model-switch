# OpenClaw Skill: Model Switcher 🔄

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that lets you switch AI models for the current session via a simple text menu.

## ✨ Features

- **Text-based menu** — clean numbered list, no inline buttons
- **Alias support** — switch by number, name, or alias (e.g. `gemini`, `opus`)
- **Lightweight** — pure bash + jq, no Python dependency
- **Reset** — option 0 to return to the default model

## 📦 Requirements

- [OpenClaw](https://github.com/openclaw/openclaw)
- `jq` (usually pre-installed on macOS; `apt install jq` on Linux)

## 🚀 Installation

Clone into your OpenClaw workspace's `skills` folder:

```bash
git clone https://github.com/rin4096/openclaw-skill-model-switch.git skills/model-switcher
```

OpenClaw will automatically detect the skill.

## 🎮 Usage

Say any of:
- "切換模型" / "switch model" / "list models"
- "use gemini" / "用 flash"

The agent will display a numbered menu. Reply with a number to switch.

### Example Output

```
🔄 模型切換選單

✨ 共有 5 個可用模型：

1️⃣  anthropic/claude-opus-4-6
    別名: opus (默認) ✨

2️⃣  google/gemini-3-flash-preview
    別名: gemini-flash

3️⃣  google/gemini-3-pro-preview
    別名: gemini

...

──────────────

0️⃣  重置為默認模型

💡 回覆編號（0-5）即可切換
```

## 🛠 How It Works

1. Script reads `openclaw config get agents.defaults` to get the model list
2. Formats a numbered text menu with aliases and default marker
3. Agent captures user's reply and calls `session_status(model=...)` to switch

## 📁 Structure

```
skills/model-switcher/
├── README.md
├── SKILL.md
└── scripts/
    └── model-switcher.sh
```

---

Created with 💕 by [Akiyama Mizuki](https://github.com/rin4096) 🎀
