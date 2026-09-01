#!/bin/bash
set -e

DEFAULT_COMMIT_MSG="日常更新 $(date '+%Y-%m-%d %H:%M:%S')"
COMMIT_MSG="${1:-$DEFAULT_COMMIT_MSG}"

echo "📝 提交信息：$COMMIT_MSG"

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "❌ 当前目录不是 Git 仓库"
    exit 1
fi

echo "🎨 运行 Black 格式化..."
black .

if [[ -z $(git status --porcelain) ]]; then
    echo "✅ 没有需要提交的更改"
    exit 0
fi

echo "----- 待提交的文件 -----"
git status --short
echo "------------------------"

git add .
git commit -m "$COMMIT_MSG"

BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "master")
echo "🚀 推送到 origin/$BRANCH ..."
git push origin "$BRANCH"

echo "🎉 更新完成！"