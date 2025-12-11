from app.services.llm_service import LLMService
import os

def test_stub_response(monkeypatch):
    os.environ["LLM_PROVIDER"] = "stub"
    svc = LLMService()
    svc.provider = "stub"
    text, tokens = svc.get_response([{"role":"user","content":"hi"}])
    assert text == "stub response"
    assert tokens == 0
