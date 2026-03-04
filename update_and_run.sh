#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$PROJECT_DIR/frontend"
API_DIR="$PROJECT_DIR"

# 输出带颜色的信息
info() {
    echo -e "${GREEN}[信息] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[警告] $1${NC}"
}

error() {
    echo -e "${RED}[错误] $1${NC}"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        error "$1 命令未找到，请安装后再试。"
        exit 1
    fi
}

# 检查必要的命令
check_command "git"
check_command "npm"
check_command "python3"

# 从GitHub更新代码
update_code() {
    info "正在从GitHub更新代码..."
    cd "$PROJECT_DIR"
    
    # 检查是否有未提交的更改
    if [ -n "$(git status --porcelain)" ]; then
        warning "本地有未提交的更改，将先暂存这些更改"
        git stash
        local stashed=true
    fi
    
    # 拉取最新代码
    if git pull; then
        info "代码更新成功"
        
        # 如果之前有暂存的更改，现在应用回来
        if [ "$stashed" = true ]; then
            warning "正在恢复之前的本地更改"
            git stash pop
            if [ $? -ne 0 ]; then
                error "恢复本地更改时发生冲突，请手动解决"
            fi
        fi
    else
        error "代码更新失败，请检查网络或仓库状态"
        exit 1
    fi
}

# 安装API依赖
install_api_deps() {
    info "正在安装API依赖..."
    cd "$API_DIR"
    
    # 检查虚拟环境是否存在，不存在则创建
    if [ ! -d "venv" ]; then
        info "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境并安装依赖
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r requirements_api.txt
    
    if [ $? -eq 0 ]; then
        info "API依赖安装成功"
    else
        error "API依赖安装失败"
        exit 1
    fi
}

# 安装前端依赖
install_frontend_deps() {
    info "正在安装前端依赖..."
    cd "$FRONTEND_DIR"
    
    npm install
    
    if [ $? -eq 0 ]; then
        info "前端依赖安装成功"
    else
        error "前端依赖安装失败"
        exit 1
    fi
}

# 启动API服务器
start_api() {
    info "正在启动API服务器..."
    cd "$API_DIR"
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 在后台启动API服务器
    python3 server.py &
    API_PID=$!
    
    # 等待服务器启动
    sleep 3
    
    if ps -p $API_PID > /dev/null; then
        info "API服务器启动成功，运行在 http://localhost:5000"
    else
        error "API服务器启动失败"
        exit 1
    fi
}

# 启动Vue前端
start_frontend() {
    info "正在启动Vue前端..."
    cd "$FRONTEND_DIR"
    
    # 在后台启动Vue开发服务器
    npm run dev &
    FRONTEND_PID=$!
    
    # 等待服务器启动
    sleep 5
    
    if ps -p $FRONTEND_PID > /dev/null; then
        info "Vue前端启动成功，运行在 http://localhost:3001"
    else
        error "Vue前端启动失败"
        exit 1
    fi
}

# 定时更新代码函数
auto_update() {
    while true; do
        info "正在执行定时代码更新..."
        update_code
        info "下次更新将在1分钟后进行"
        sleep 60
    done
}

# 主函数
main() {
    info "=== 开始执行自动化脚本 ==="
    
    update_code
    install_api_deps
    install_frontend_deps
    start_api
    start_frontend
    
    info "=== 所有服务已启动 ==="
    info "API服务器: http://localhost:5000"
    info "Vue前端: http://localhost:3001"
    info "自动更新已启用，每分钟更新一次代码"
    info "按 Ctrl+C 停止所有服务"
    
    # 在后台启动自动更新
    auto_update &
    UPDATE_PID=$!
    
    # 等待用户中断
    wait
}

# 清理函数，当脚本被中断时执行
cleanup() {
    info "正在停止所有服务..."
    
    # 找到并杀死API进程
    pkill -f "python server.py" || true
    
    # 找到并杀死Vue开发服务器进程
    pkill -f "vite" || true
    
    # 如果存在自动更新进程，杀死它
    if [ -n "$UPDATE_PID" ]; then
        kill $UPDATE_PID 2>/dev/null || true
    fi
    
    info "所有服务已停止"
    exit 0
}

# 注册清理函数
trap cleanup INT TERM

# 执行主函数
main
