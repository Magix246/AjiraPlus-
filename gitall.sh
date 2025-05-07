#!/bin/bash

echo "🔄 Kuanza kupakua mabadiliko kutoka GitHub..."
git pull origin main

echo "➕ Kuongeza faili zote mpya au zilizobadilika..."
git add .

echo "✍️ Andika ujumbe wa commit (kisha bonyeza ENTER):"
read msg

git commit -m "$msg"

echo "📤 Kutuma mabadiliko yako kwenda GitHub..."
git push origin main

echo "✅ Kazi imekamilika kwa mafanikio!"
