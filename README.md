# OpenClaw Skill: Model Switcher 🎭

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that allows you to dynamically switch the AI model for the current session without modifying `openclaw.json`.

## ✨ Features

- **Interactive Menu**: Use `/switch-model` to get a list of available models as Telegram buttons.
- **Direct Commands**: Switch models by name or alias (e.g., "switch to flash", "use pro").
- **Fuzzy Search**: Supports searching for models by keywords.
- **Session-Specific**: Changes only apply to the current session. Starting a new session (`/new`) resets to system defaults.

## 🚀 Installation

1. Clone this repository into your OpenClaw workspace's `skills` folder:
   ```bash
   git clone https://github.com/rin4096/openclaw-skill-model-switch.git skills/model-switch
   ```
2. OpenClaw will automatically detect the skill.

## 🎮 Usage

- `/switch-model`: Displays the interactive model selection menu.
- `切换模型到 flash`: Switches to the model aliased as "flash".
- `用 pro 模型`: Switches to the model aliased as "pro".
- `重置模型`: Removes the session override and returns to the default model.

## 🤖 Model Aliases

By default, the skill recognizes:
- `flash` -> `google/gemini-3-flash-preview`
- `pro` -> `google/gemini-3-pro-preview`
- `default` -> Resets to system default

## 🛠 Technical Details

The skill uses OpenClaw's `session_status(model="...")` tool to perform the override. It dynamically reads the available models from your `openclaw.json` using the included `list_models.py` script.

---
Created with love by [Akiyama Mizuki](https://github.com/openclaw/openclaw) for Ena. 🎀
