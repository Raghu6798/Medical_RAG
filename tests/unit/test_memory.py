import pytest
from routes.query_route import get_memory

def test_get_memory_instance():
    session_id = "test-session"
    memory = get_memory(session_id)
    assert memory is not None
    assert hasattr(memory, "add_message")
    assert hasattr(memory, "messages")
