#!/bin/bash

echo "🔄 Kukagua mabadiliko..."
git status

echo "➕ Kuongeza faili zote..."
git add .

echo "✍️  Andika ujumbe wa commit (kisha bonyeza ENTER):"
read msg

git commit -m "$msg"

echo "📤 Kutuma mabadiliko kwenye GitHub..."
git push origin main

echo "✅ Mabadiliko yametumwa kwa mafanikio!"
