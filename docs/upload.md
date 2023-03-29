# 简介

本文主要介绍如何上传改安装包到pypi

## 步骤

```sh
#进入vmilog-py路径下
cd ./vmilog-py

# 安装twine
pip install twine

# 编译安装包
python setup.py sdist

#上传
twine ./dist/*
```