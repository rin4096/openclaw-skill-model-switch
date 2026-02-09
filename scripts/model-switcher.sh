#!/usr/bin/env bash
#
# Model Switcher — 純文字選單
# 列出所有可用模型，標記當前模型
#

set -euo pipefail

if ! command -v openclaw &>/dev/null; then
    echo "❌ 找不到 openclaw 命令"
    exit 1
fi

if ! command -v jq &>/dev/null; then
    echo "❌ 找不到 jq 命令"
    exit 1
fi

CONFIG=$(openclaw config get agents.defaults 2>&1)

if [[ -z "$CONFIG" ]] || ! echo "$CONFIG" | jq empty 2>/dev/null; then
    echo "❌ 無法獲取配置"
    exit 1
fi

PRIMARY=$(echo "$CONFIG" | jq -r '.model.primary // ""')
MODELS=$(echo "$CONFIG" | jq -r '.models | keys[]')

count=0
while IFS= read -r _; do
    ((count++))
done <<< "$MODELS"

echo "🔄 模型切換選單"
echo ""
echo "✨ 共有 ${count} 個可用模型："
echo ""

i=1
while IFS= read -r model_id; do
    alias=$(echo "$CONFIG" | jq -r --arg m "$model_id" '.models[$m].alias // ""')

    marker=""
    if [[ "$model_id" == "$PRIMARY" ]]; then
        marker=" (默認) ✨"
    fi

    # 顯示模型
    echo "${i}️⃣  ${model_id}"
    if [[ -n "$alias" ]]; then
        echo "    別名: ${alias}${marker}"
    elif [[ -n "$marker" ]]; then
        echo "   ${marker}"
    fi
    echo ""
    ((i++))
done <<< "$MODELS"

echo "──────────────"
echo ""
echo "0️⃣  重置為默認模型"
echo ""
echo "💡 回覆編號（0-${count}）即可切換"
