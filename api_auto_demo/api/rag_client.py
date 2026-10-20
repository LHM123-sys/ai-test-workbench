# -*- coding: utf-8 -*-
"""RAG 客服接口封装：把调 DeepSeek 的逻辑包成一个 client"""
import os

import requests


class RagClient:
    def __init__(self, base_url, model, temperature, timeout):
        self.url = f"{base_url}/chat/completions"
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.key = os.environ.get("DEEPSEEK_API_KEY")

    def ask(self, question, contexts=None):
        """发一个问题，返回回答文本"""
        if contexts is None:
            contexts = []
        prompt = f"已知信息：{contexts}\n问题：{question}\n知识库没有就拒答。"
        r = requests.post(
            self.url,
            headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
            json={"model": self.model, "temperature": self.temperature,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
