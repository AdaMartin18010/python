#!/bin/bash
# Python 2025开发环境一键安装脚本
# 
# 功能：
# - 安装uv包管理器
# - 安装Python 3.12
# - 配置常用工具（ruff, mypy, pytest等）
# - 设置pre-commit钩子
# 
# 使用方式：
#   chmod +x setup_dev_env.sh
#   ./setup_dev_env.sh

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Python 2025 开发环境安装脚本${NC}"
echo -e "${BLUE}========================================${NC}\n"

# 检测操作系统
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo -e "${YELLOW}检测到操作系统: $OS${NC}\n"

# ============ 1. 安装uv ============

echo -e "${GREEN}[1/6] 安装uv包管理器...${NC}"

if command -v uv &> /dev/null; then
    echo "  ✓ uv已安装: $(uv --version)"
else
    echo "  正在下载并安装uv..."
    if [[ "$OS" == "windows" ]]; then
        powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    echo "  ✓ uv安装完成"
fi

# 刷新PATH
export PATH="$HOME/.cargo/bin:$PATH"

# ============ 2. 安装Python 3.12 ============

echo -e "\n${GREEN}[2/6] 检查Python 3.12...${NC}"

if command -v python3.12 &> /dev/null; then
    echo "  ✓ Python 3.12已安装: $(python3.12 --version)"
else
    echo "  Python 3.12未找到"
    
    if [[ "$OS" == "macos" ]]; then
        echo "  使用Homebrew安装Python 3.12..."
        brew install python@3.12
    elif [[ "$OS" == "linux" ]]; then
        echo "  使用apt安装Python 3.12..."
        sudo apt update
        sudo apt install -y python3.12 python3.12-venv python3.12-dev
    else
        echo -e "${YELLOW}  请手动从 https://www.python.org/downloads/ 下载安装${NC}"
        exit 1
    fi
    
    echo "  ✓ Python 3.12安装完成"
fi

# ============ 3. 创建虚拟环境 ============

echo -e "\n${GREEN}[3/6] 创建虚拟环境...${NC}"

if [ -d ".venv" ]; then
    echo "  ✓ 虚拟环境已存在"
else
    uv venv --python 3.12
    echo "  ✓ 虚拟环境创建完成"
fi

# 激活虚拟环境
if [[ "$OS" == "windows" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# ============ 4. 安装开发依赖 ============

echo -e "\n${GREEN}[4/6] 安装开发依赖...${NC}"

echo "  安装核心工具..."
uv pip install --upgrade pip

# 代码质量工具
echo "  - 安装ruff (代码检查和格式化)..."
uv pip install ruff==0.6.0

echo "  - 安装mypy (类型检查)..."
uv pip install mypy==1.11.0

# 测试工具
echo "  - 安装pytest及插件..."
uv pip install \
    pytest==8.3.0 \
    pytest-cov==5.0.0 \
    pytest-asyncio==0.24.0 \
    pytest-mock==3.14.0

# 预提交钩子
echo "  - 安装pre-commit..."
uv pip install pre-commit==3.8.0

echo "  ✓ 开发依赖安装完成"

# ============ 5. 配置工具 ============

echo -e "\n${GREEN}[5/6] 配置开发工具...${NC}"

# 配置pre-commit
if [ -f ".pre-commit-config.yaml" ]; then
    echo "  配置pre-commit钩子..."
    pre-commit install
    echo "  ✓ pre-commit钩子已安装"
else
    echo -e "  ${YELLOW}未找到.pre-commit-config.yaml，跳过pre-commit配置${NC}"
fi

# 配置git（如果存在）
if [ -d ".git" ]; then
    echo "  配置git..."
    
    # 设置换行符
    git config core.autocrlf input
    
    # 忽略权限变化
    git config core.filemode false
    
    echo "  ✓ git配置完成"
fi

# ============ 6. 验证安装 ============

echo -e "\n${GREEN}[6/6] 验证安装...${NC}"

echo "  Python版本:"
python --version

echo -e "\n  已安装的工具:"
echo "  - uv: $(uv --version 2>&1 | head -n 1)"
echo "  - ruff: $(ruff --version)"
echo "  - mypy: $(mypy --version)"
echo "  - pytest: $(pytest --version)"

# ============ 完成 ============

echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}✓ 开发环境安装完成！${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo "下一步操作:"
echo "  1. 激活虚拟环境:"
if [[ "$OS" == "windows" ]]; then
    echo "     .venv\\Scripts\\activate"
else
    echo "     source .venv/bin/activate"
fi
echo ""
echo "  2. 安装项目依赖:"
echo "     uv sync"
echo ""
echo "  3. 运行代码检查:"
echo "     ruff check ."
echo "     mypy ."
echo ""
echo "  4. 运行测试:"
echo "     pytest"
echo ""
echo "  5. 查看帮助:"
echo "     cat README.md"
echo ""

# 创建便捷脚本
echo -e "${YELLOW}创建便捷脚本...${NC}"

# 代码检查脚本
cat > check.sh << 'EOF'
#!/bin/bash
# 代码质量检查脚本

echo "🔍 Running code checks..."

echo ""
echo "1️⃣  Ruff (linting)..."
ruff check .

echo ""
echo "2️⃣  Mypy (type checking)..."
mypy .

echo ""
echo "3️⃣  Pytest (testing)..."
pytest

echo ""
echo "✅ All checks completed!"
EOF

chmod +x check.sh

echo "  ✓ 创建了 check.sh 脚本（运行所有检查）"

# 格式化脚本
cat > format.sh << 'EOF'
#!/bin/bash
# 代码格式化脚本

echo "✨ Formatting code..."

ruff check --fix .
ruff format .

echo "✅ Code formatted!"
EOF

chmod +x format.sh

echo "  ✓ 创建了 format.sh 脚本（格式化代码）"

echo -e "\n${GREEN}安装完成！享受Python 2025开发之旅！🚀${NC}\n"

