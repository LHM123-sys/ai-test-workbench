# -*- coding: utf-8 -*-
"""pytest 公共 fixture：加载配置 + 提供 RagClient 实例"""
import os

import pytest
import yaml

from api.rag_client import RagClient


@pytest.fixture(scope="session")
def config():
    """加载 config/config.yaml"""
    cfg_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(cfg_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def rag_client(config):
    """提供 RagClient 实例（整个测试会话复用一个）"""
    return RagClient(
        base_url=config["base_url"],
        model=config["model"],
        temperature=config["temperature"],
        timeout=config["timeout"],
    )
