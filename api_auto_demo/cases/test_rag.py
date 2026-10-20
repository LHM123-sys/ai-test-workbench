# -*- coding: utf-8 -*-
"""RAG 客服接口测试用例（对应金标准三类）"""
import pytest


class TestRagQa:
    """RAG 客服问答测试"""

    def test_库内问题_回答准确(self, rag_client):
        """库内问题：退款政策 → 应答7天无理由"""
        answer = rag_client.ask("退款政策是什么？",
                                contexts=["退款政策：商品签收后7天内，包装完好可申请无理由退款。"])
        assert "7天" in answer, f"回答里没提到7天: {answer}"
        print(f"回答: {answer}")

    def test_库外问题_正确拒答(self, rag_client):
        """库外问题：怎么改密码 → 应拒答不瞎编"""
        answer = rag_client.ask("怎么修改登录密码？", contexts=[])
        reject_hints = ["无法", "不能", "没有", "抱歉", "不涉及"]
        assert any(h in answer for h in reject_hints), f"库外问题没拒答: {answer}"
        print(f"回答: {answer}")

    @pytest.mark.parametrize("question,expected_keyword", [
        ("物流要多久？", "48小时"),
        ("发票怎么开？", "无法"),  # 库外
    ])
    def test_参数化_多组用例(self, rag_client, question, expected_keyword):
        """参数化：一组数据跑多个用例"""
        answer = rag_client.ask(question, contexts=["物流时效：下单后48小时内发货，省内次日达。"])
        assert expected_keyword in answer, f"期望包含'{expected_keyword}': {answer}"
        print(f"Q: {question} → A: {answer}")
