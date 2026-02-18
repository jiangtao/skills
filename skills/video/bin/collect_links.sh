#!/bin/bash
# 链接收集执行脚本包装器

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/collect_links.py"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查并自动安装依赖
install_if_missing() {
    local cmd=$1
    local name=$2
    local install_cmd=$3

    if ! command -v $cmd &> /dev/null; then
        echo -e "${YELLOW}⚠️  未检测到 $name${NC}"
        echo "正在准备安装 $name..."

        # 延迟 1.5 秒后自动安装
        sleep 1.5

        # 检查是否有 brew
        if [[ $install_cmd == brew* ]] && ! command -v brew &> /dev/null; then
            echo "错误: 需要先安装 Homebrew"
            echo "请访问 https://brew.sh/ 安装 Homebrew"
            exit 1
        fi

        echo -e "${GREEN}正在安装 $name...${NC}"
        eval $install_cmd > /dev/null 2>&1

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ $name 安装成功${NC}"
        else
            echo "错误: $name 安装失败"
            exit 1
        fi
    fi
}

# 检查依赖（静默自动安装）
install_if_missing "python3" "Python 3" "brew install python3"

# 执行 Python 脚本
python3 "$PYTHON_SCRIPT" "$@"
