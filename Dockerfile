# 使用官方Python镜像作为基础镜像
FROM python:3.10-bookworm

# 安装ffmpeg
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    apt-transport-https && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置Poetry环境变量
ENV POETRY_VENV=/app/.venv

# 国内清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装Poetry
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

# 设置环境变量，确保使用的是虚拟环境中的 Python 和工具
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装依赖
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root

# 将当前目录下的文件复制到容器的/app目录中
COPY . /app

# 暴露端口
EXPOSE 8000

# 设置容器启动后执行的命令
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]