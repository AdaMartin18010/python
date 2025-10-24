#!/bin/bash
# Python 2025示例程序运行脚本
#
# 快速运行各个章节的示例程序

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Python 2025 示例程序运行器${NC}"
echo -e "${BLUE}========================================${NC}\n"

# 显示菜单
show_menu() {
    echo "请选择要运行的示例:"
    echo ""
    echo "  ${GREEN}监控与可观测性:${NC}"
    echo "    1) 完整监控示例 (Prometheus + OpenTelemetry + Structlog)"
    echo ""
    echo "  ${GREEN}安全与合规:${NC}"
    echo "    2) 安全API示例 (认证 + 授权 + 速率限制)"
    echo ""
    echo "  ${GREEN}性能优化与压测:${NC}"
    echo "    3) Locust压测 (Web界面)"
    echo "    4) Locust压测 (命令行模式)"
    echo ""
    echo "  ${GREEN}AI集成开发:${NC}"
    echo "    5) RAG聊天机器人"
    echo ""
    echo "  ${GREEN}其他:${NC}"
    echo "    6) 运行所有健康检查"
    echo "    0) 退出"
    echo ""
}

# 检查依赖
check_dependencies() {
    local example=$1
    echo -e "${YELLOW}检查依赖...${NC}"
    
    case $example in
        1)
            uv pip install fastapi[standard] prometheus-client opentelemetry-api opentelemetry-sdk structlog
            ;;
        2)
            uv pip install fastapi[standard] pydantic python-jose[cryptography] passlib[bcrypt] python-multipart
            ;;
        3|4)
            uv pip install locust
            ;;
        5)
            uv pip install langchain langchain-openai langchain-community qdrant-client tiktoken
            ;;
    esac
    
    echo -e "${GREEN}✓ 依赖检查完成${NC}\n"
}

# 运行示例 1: 监控应用
run_monitoring_example() {
    echo -e "${GREEN}启动监控示例应用...${NC}"
    echo "  URL: http://localhost:8000"
    echo "  指标: http://localhost:8000/metrics"
    echo "  文档: http://localhost:8000/docs"
    echo ""
    echo "按 Ctrl+C 停止"
    echo ""
    
    check_dependencies 1
    cd python/07-监控与可观测性/examples
    uvicorn complete_monitoring_app:app --reload
}

# 运行示例 2: 安全API
run_security_example() {
    echo -e "${GREEN}启动安全API示例...${NC}"
    echo "  URL: http://localhost:8000"
    echo "  文档: http://localhost:8000/docs"
    echo ""
    echo "测试账号:"
    echo "  用户名: admin, 密码: Admin123!@#"
    echo "  用户名: testuser, 密码: Test123!@#"
    echo ""
    echo "按 Ctrl+C 停止"
    echo ""
    
    check_dependencies 2
    cd python/08-安全与合规/examples
    uvicorn secure_api_example:app --reload
}

# 运行示例 3: Locust Web界面
run_locust_web() {
    echo -e "${GREEN}启动Locust压测 (Web界面)...${NC}"
    echo "  Locust UI: http://localhost:8089"
    echo ""
    echo "使用说明:"
    echo "  1. 访问 http://localhost:8089"
    echo "  2. 设置用户数和生成速率"
    echo "  3. 输入目标地址: http://localhost:8000"
    echo "  4. 点击 Start swarming"
    echo ""
    echo "按 Ctrl+C 停止"
    echo ""
    
    check_dependencies 3
    cd python/09-性能优化与压测/examples
    locust -f locustfile.py --host=http://localhost:8000
}

# 运行示例 4: Locust命令行
run_locust_cli() {
    echo -e "${GREEN}启动Locust压测 (命令行模式)...${NC}"
    echo "  配置: 100用户, 10用户/秒, 运行5分钟"
    echo ""
    
    check_dependencies 4
    cd python/09-性能优化与压测/examples
    locust -f locustfile.py \
        --host=http://localhost:8000 \
        --users=100 \
        --spawn-rate=10 \
        --run-time=5m \
        --headless \
        --html=report.html
    
    echo ""
    echo -e "${GREEN}✓ 压测完成！${NC}"
    echo "  查看报告: report.html"
}

# 运行示例 5: RAG聊天机器人
run_rag_chatbot() {
    echo -e "${GREEN}启动RAG聊天机器人...${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  需要设置 OPENAI_API_KEY 环境变量${NC}"
    echo ""
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "请先设置API密钥:"
        echo "  export OPENAI_API_KEY='your-api-key'"
        echo ""
        read -p "是否继续? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    check_dependencies 5
    cd python/10-AI集成开发/examples
    python rag_chatbot.py
}

# 运行示例 6: 健康检查
run_health_checks() {
    echo -e "${GREEN}运行所有健康检查...${NC}\n"
    
    # Python版本
    echo "Python版本:"
    python --version
    echo ""
    
    # 工具版本
    echo "开发工具:"
    echo "  - uv: $(uv --version 2>&1 | head -n 1 || echo '未安装')"
    echo "  - ruff: $(ruff --version || echo '未安装')"
    echo "  - mypy: $(mypy --version || echo '未安装')"
    echo "  - pytest: $(pytest --version || echo '未安装')"
    echo ""
    
    # 运行测试
    echo "运行单元测试..."
    if [ -d "tests" ]; then
        pytest tests/ -v
    else
        echo "  未找到tests目录"
    fi
    echo ""
    
    # 代码检查
    echo "运行代码检查..."
    ruff check . --quiet && echo "  ✓ Ruff检查通过" || echo "  ✗ Ruff检查失败"
    mypy . --quiet && echo "  ✓ Mypy检查通过" || echo "  ✗ Mypy检查失败"
    echo ""
    
    echo -e "${GREEN}✓ 健康检查完成${NC}"
}

# 主循环
while true; do
    show_menu
    read -p "请选择 [0-6]: " choice
    echo ""
    
    case $choice in
        1)
            run_monitoring_example
            ;;
        2)
            run_security_example
            ;;
        3)
            run_locust_web
            ;;
        4)
            run_locust_cli
            ;;
        5)
            run_rag_chatbot
            ;;
        6)
            run_health_checks
            read -p "按Enter继续..."
            ;;
        0)
            echo "退出"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}无效选择，请重试${NC}\n"
            ;;
    esac
    
    echo ""
done

