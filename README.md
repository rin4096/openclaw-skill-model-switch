# OpenClaw Skill: Model Switcher 🎭

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that allows you to dynamically switch the AI model for the current session without modifying `openclaw.json`.

## ✨ Features

- **Official Catalog Support**: Prioritizes models defined in `agents.defaults.models` following the OpenClaw standard.
- **Interactive Menu**: Use `/switch-model` to get a list of available models as Telegram buttons, enriched with model descriptions.
- **Smart Search**: Switch models using keywords, aliases, or tags (e.g., "switch to code model", "use flash").
- **Metadata Aware**: Displays descriptions and tags to help you choose the right model.

## 🚀 Installation

1. Clone this repository into your OpenClaw workspace's `skills` folder:
   ```bash
   git clone https://github.com/rin4096/openclaw-skill-model-switch.git skills/model-switch
   ```
2. OpenClaw will automatically detect the skill.

## 🎮 Usage

- `/switch-model`: Displays the interactive model selection menu.
- `Switch model to flash`: Switches to the model aliased as "flash".
- `Use the pro model`: Switches to the model aliased as "pro".
- `Reset model`: Removes the session override and returns to the default model.

## 🤖 Model Aliases

By default, the skill recognizes:
- `flash` -> `google/gemini-3-flash-preview`
- `pro` -> `google/gemini-3-pro-preview`
- `default` -> Resets to system default

## 🛠 Technical Details

The skill uses OpenClaw's `session_status(model="...")` tool to perform the override. It dynamically reads the available models from your `openclaw.json` using the included `list_models.py` script.

---
Created with love by [Akiyama Mizuki](https://github.com/openclaw/openclaw) for Ena. 🎀
