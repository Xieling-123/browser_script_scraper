# browser_script_scraper

## 环境恢复

### 方式一：使用 requirements.txt（推荐，精确恢复）
1. 创建并激活虚拟环境（如尚未创建）：
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows Git Bash
   # 或 Linux/Mac: source venv/bin/activate
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 方式二：使用 pyproject.toml（开发模式）
```bash
pip install -e .
```

## 运行项目
```bash
python src/main.py
```

## 使用 VS Code 任务
- 按 `Ctrl+Shift+P` → "Tasks: Run Task" → 选择任务。

## 依赖管理
- 项目依赖定义在 `pyproject.toml` 的 `[project] dependencies` 中。
- 完整环境依赖（含传递依赖）固定在 `requirements.txt` 中，由脚本自动生成。
