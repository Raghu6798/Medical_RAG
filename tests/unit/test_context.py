import pytest
from routes.query_route import get_retrieved_context # Adjust path as needed

class DummyRetriever:
    def invoke(self, query):
        return [
            type("Doc", (), {"page_content": "This is a test doc."}),
            type("Doc", (), {"page_content": "Second doc."}),
        ]

def test_get_retrieved_context(monkeypatch):
    monkeypatch.setattr("your_module.retriever", DummyRetriever())
    result = get_retrieved_context("What is diabetes?")
    assert "This is a test doc." in result
    assert "Second doc." in result
