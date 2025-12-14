import os

os.system('py -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/')
os.system('pip install --upgrade uv ruff -i https://mirrors.aliyun.com/pypi/simple/')
os.system('xmake update')
os.system('rustup update')
