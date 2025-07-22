#!/usr/bin/env bash

# 全局一键管理脚本，提升开发执行体验
# 用法： ./manage.sh [start|stop|test|import_provinces|status]

# 项目路径
FRONTEND_DIR="frontend"
BACKEND_DIR="backend"
CONDA_ENV="kaodian"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function activate_env() {
    if command -v conda &>/dev/null; then
        echo -e "${YELLOW}自动激活conda环境: $CONDA_ENV${NC}"
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate $CONDA_ENV
    elif [ -f "$BACKEND_DIR/venv/bin/activate" ]; then
        echo -e "${YELLOW}自动激活venv环境${NC}"
        source "$BACKEND_DIR/venv/bin/activate"
    else
        echo -e "${RED}未检测到conda或venv环境，请手动激活！${NC}"
    fi
}

function kill_port() {
    local port=$1
    local pname=$2
    pid=$(lsof -ti tcp:$port)
    if [ ! -z "$pid" ]; then
        echo -e "${YELLOW}检测到$port端口被占用，自动释放...${NC}"
        kill -9 $pid && echo -e "${GREEN}$pname端口$port已释放${NC}" || echo -e "${RED}释放$pname端口$port失败${NC}"
    fi
}

function start_all() {
    activate_env
    kill_port 8000 "后端"
    kill_port 3000 "前端"
    kill_port 5173 "前端"
    echo -e "${GREEN}启动后端服务...${NC}"
    cd $BACKEND_DIR && nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    cd - >/dev/null
    echo -e "${GREEN}启动前端服务...${NC}"
    cd $FRONTEND_DIR && pnpm start > frontend.log 2>&1 &
    cd - >/dev/null
    echo -e "${GREEN}前后端服务已启动！${NC}"
}

function stop_all() {
    echo -e "${YELLOW}尝试停止前后端服务...${NC}"
    pkill -f "uvicorn main:app" && echo -e "${GREEN}后端已停止${NC}" || echo -e "${YELLOW}后端未运行${NC}"
    pkill -f "pnpm start" && echo -e "${GREEN}前端已停止${NC}" || echo -e "${YELLOW}前端未运行${NC}"
    kill_port 8000 "后端"
    kill_port 3000 "前端"
    kill_port 5173 "前端"
}

function run_tests() {
    activate_env
    echo -e "${YELLOW}运行后端自动化测试...${NC}"
    cd $BACKEND_DIR && pytest --maxfail=1 --disable-warnings -v
    cd - >/dev/null
}

function import_provinces() {
    activate_env
    if [ -f "$BACKEND_DIR/init_provinces.sql" ]; then
        echo -e "${YELLOW}导入省份基础数据...${NC}"
        # 需根据你的MySQL容器名和账号密码调整
        docker exec -i mysql-container mysql -uroot -pyourpassword yourdb < $BACKEND_DIR/init_provinces.sql && \
        echo -e "${GREEN}省份数据导入成功！${NC}" || echo -e "${RED}省份数据导入失败，请检查数据库连接和SQL脚本！${NC}"
    else
        echo -e "${RED}未找到init_provinces.sql！${NC}"
    fi
}

function status() {
    echo -e "${YELLOW}服务状态检查:${NC}"
    pgrep -af "uvicorn main:app" && echo -e "${GREEN}后端运行中${NC}" || echo -e "${RED}后端未运行${NC}"
    pgrep -af "pnpm start" && echo -e "${GREEN}前端运行中${NC}" || echo -e "${RED}前端未运行${NC}"
    echo -e "${YELLOW}依赖检测:${NC}"
    if ! command -v pnpm &>/dev/null; then
        echo -e "${RED}pnpm未安装${NC}"
    fi
    if ! command -v uvicorn &>/dev/null; then
        echo -e "${RED}uvicorn未安装${NC}"
    fi
    if ! command -v pytest &>/dev/null; then
        echo -e "${RED}pytest未安装${NC}"
    fi
}

case "$1" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    test)
        run_tests
        ;;
    import_provinces)
        import_provinces
        ;;
    status)
        status
        ;;
    *)
        echo -e "${YELLOW}用法: $0 [start|stop|test|import_provinces|status]${NC}"
        ;;
esac 