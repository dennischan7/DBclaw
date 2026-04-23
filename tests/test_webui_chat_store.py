from datetime import datetime

from webui import chat_store


def test_save_message_serializes_datetime_task_snapshot(tmp_path, monkeypatch):
    test_db = tmp_path / "chat_history.db"
    monkeypatch.setattr(chat_store, "_DB_PATH", test_db)
    monkeypatch.setattr(chat_store, "_conn", None)

    conversation = chat_store.create_conversation(title="serialize-test", instance_name="pg_test")

    message_id = chat_store.save_message(
        conversation["id"],
        "assistant",
        "ok",
        task_snapshot={
            "task_id": "serialize-test",
            "execution_result": {
                "rows": [
                    {"created_at": datetime(2026, 4, 22, 10, 11, 12)}
                ]
            },
        },
    )

    messages = chat_store.get_messages(conversation["id"])

    assert message_id is not None
    assert messages[-1]["task_snapshot"]["execution_result"]["rows"][0]["created_at"] == "2026-04-22T10:11:12"

    if chat_store._conn is not None:
        chat_store._conn.close()
    monkeypatch.setattr(chat_store, "_conn", None)