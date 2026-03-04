#!/bin/bash

# chmod +x monitor.sh
# nohup ./monitor.sh > monitor_output.log 2>&1 &
# 项目路径
# 根据实际情况设置项目路径
PROJECT_PATH="$(cd "$(dirname "$0")" && pwd)"
# 如果在服务器上运行，可以手动设置为固定路径
# PROJECT_PATH="/root/AI-Agent-Debate"
FRONTEND_PATH="$PROJECT_PATH/frontend"
LOG_FILE="$PROJECT_PATH/monitor.log"

# 记录日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查目录是否存在
if [ ! -d "$PROJECT_PATH" ]; then
    log "项目目录不存在，正在克隆..."
    mkdir -p $(dirname "$PROJECT_PATH")
    cd $(dirname "$PROJECT_PATH")
    git clone git@github.com:FicoHu/AI-Agent-Debate.git
    if [ $? -ne 0 ]; then
        log "克隆仓库失败"
        exit 1
    fi
    log "仓库克隆成功"
fi

# 检查Python服务器是否在运行
check_python_server() {
    # 使用更精确的模式匹配，包含多种可能的进程名称
    # 先使用ps -ef，如果失败则尝试ps aux，再失败则尝试pgrep
    if ! { ps -ef | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep > /dev/null || 
           ps aux | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep > /dev/null || 
           pgrep -f "python.*app\.py|python3.*app\.py|flask.*app\.py" > /dev/null; }; then
        log "检测到Python服务器未运行，正在启动..."
        cd "$PROJECT_PATH"
        # 确保安装了必要的依赖
        pip3 install flask flask-cors bs4 requests pillow > /dev/null 2>&1 || { log "使用pip3失败，尝试pip"; pip install flask flask-cors bs4 requests pillow > /dev/null 2>&1; }
        # 使用绝对路径启动服务器
        # 尝试使用python3，如果失败则使用python
        if command -v python3 > /dev/null 2>&1; then
            log "使用python3启动服务器"
            nohup python3 "$PROJECT_PATH/flask/app.py" > "$PROJECT_PATH/server.log" 2>&1 &
        else
            log "使用python启动服务器"
            nohup python "$PROJECT_PATH/flask/app.py" > "$PROJECT_PATH/server.log" 2>&1 &
        fi
        sleep 2 # 等待服务器启动
        if { ps -ef | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep > /dev/null || 
             ps aux | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep > /dev/null || 
             pgrep -f "python.*app\.py|python3.*app\.py|flask.*app\.py" > /dev/null; }; then
            log "Python服务器启动成功"
        else
            log "Python服务器启动失败，请查看日志: $PROJECT_PATH/server.log"
        fi
    else
        # 获取并打印Python进程的进程ID
        log "获取Python进程号..."
        PYTHON_PID=$(ps -ef | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
        # 如果还是没有获取到，尝试其他方法
        if [ -z "$PYTHON_PID" ]; then
            PYTHON_PID=$(pgrep -f "python.*app\.py|python3.*app\.py|flask.*app\.py" | tr '\n' ',' | sed 's/,$//')
        fi
        # 如果还是没有，尝试直接使用pidof
        if [ -z "$PYTHON_PID" ]; then
            PYTHON_PID=$(pidof python3 python flask 2>/dev/null | tr ' ' ',' | sed 's/,$//')
        fi
        log "Python服务器正在运行中，进程ID: $PYTHON_PID"
    fi
}

# 拉取最新代码
pull_latest_code() {
    log "正在拉取最新代码..."
    cd "$PROJECT_PATH"
    
    # 检查本地是否有未提交的更改，如果有，则跳过拉取
    if git status --porcelain | grep -q '^\s*[MADRC]'; then
        log "发现本地有未提交的更改，跳过代码拉取"
        return 0
    fi
    
    # 尝试拉取最新代码
    git pull
    if [ $? -ne 0 ]; then
        log "拉取代码失败，尝试重置本地更改..."
        # 如果拉取失败，尝试强制重置
        git fetch origin
        git reset --hard origin/main
        if [ $? -ne 0 ]; then
            log "重置失败，请手动检查仓库状态"
            return 1
        else
            log "重置成功，现在代码与远程仓库一致"
        fi
    else
        log "代码拉取成功"
    fi
    
    return 0
}

# 检查npm run dev进程
check_and_start_dev_server() {
    log "检查npm run dev进程..."
    # 使用更精确的模式匹配，包含多种可能的进程名称
    if ! { ps -ef | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep > /dev/null || 
           ps aux | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep > /dev/null || 
           pgrep -f "node.*dev|vite|npm.*run.*dev" > /dev/null; }; then
        log "npm run dev进程不存在，正在启动..."
        cd "$FRONTEND_PATH"
        # 确保安装了必要的依赖
        npm install > /dev/null 2>&1
        # 使用nohup启动前端服务器
        nohup npm run dev -- --host > "$PROJECT_PATH/frontend.log" 2>&1 &
        sleep 5 # 等待前端服务器启动
        if { ps -ef | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep > /dev/null || 
             ps aux | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep > /dev/null || 
             pgrep -f "node.*dev|vite|npm.*run.*dev" > /dev/null; }; then
            log "npm run dev启动成功"
        else
            log "npm run dev启动失败，请查看日志: $PROJECT_PATH/frontend.log"
            return 1
        fi
    else
        # 获取并打印npm进程的进程ID
        log "获取npm进程号..."
        NPM_PID=$(ps -ef | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
        # 如果还是没有获取到，尝试其他方法
        if [ -z "$NPM_PID" ]; then
            NPM_PID=$(pgrep -f "node.*dev|vite|npm.*run.*dev" | tr '\n' ',' | sed 's/,$//')
        fi
        # 如果还是没有，尝试直接使用pidof
        if [ -z "$NPM_PID" ]; then
            NPM_PID=$(pidof node npm 2>/dev/null | tr ' ' ',' | sed 's/,$//')
        fi
        log "npm run dev进程正在运行中，进程ID: $NPM_PID"
    fi
    return 0
}

# 添加错误处理函数
handle_error() {
    log "脚本遇到错误，尝试恢复..."
    # 尝试杀死可能卡住的进程
    # 使用多种方法尝试杀死进程
    { ps -ef | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || 
      ps aux | grep -E 'python.*app\.py|python3.*app\.py|flask.*app\.py' | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || 
      pgrep -f "python.*app\.py|python3.*app\.py|flask.*app\.py" | xargs kill -9 2>/dev/null; } || true
    
    { ps -ef | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || 
      ps aux | grep -E 'node.*dev|vite|npm.*run.*dev' | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || 
      pgrep -f "node.*dev|vite|npm.*run.*dev" | xargs kill -9 2>/dev/null; } || true
    log "清理完成，将重新启动服务"
}

# 添加信号处理
trap 'handle_error' ERR
trap 'log "脚本收到终止信号，正在清理并退出..."; exit 0' SIGINT SIGTERM

# 初始化日志
log "监控脚本启动于 $(date '+%Y-%m-%d %H:%M:%S')"

# 主循环
while true; do
    pull_latest_code
    check_python_server      # 检查Python服务器是否在运行
    check_and_start_dev_server
    log "服务检查完成，等待1分钟后再次检查..."
    sleep 60
done
