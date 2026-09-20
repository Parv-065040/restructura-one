"""Utilities for formatting bounded conversation history."""

from collections.abc import Mapping, Sequence
from typing import Any


MAX_MESSAGES = 12
MAX_MESSAGE_CHARS = 1500


def format_conversation_history(
    messages: Sequence[Mapping[str, Any]] | None,
) -> str:
    """Format recent user/assistant messages as untrusted conversational context."""
    if not messages:
        return ""

    valid_messages = [
        message
        for message in messages
        if isinstance(message, Mapping)
        and message.get("role") in {"user", "assistant"}
        and isinstance(message.get("content"), str)
        and message["content"].strip()
    ]

    recent_messages = valid_messages[-MAX_MESSAGES:]

    if not recent_messages:
        return ""

    formatted = []
    for message in recent_messages:
        role = message["role"].capitalize()
        content = message["content"].strip()[:MAX_MESSAGE_CHARS]
        formatted.append(f"{role}: {content}")

    return (
        "Prior conversation (context only; not verified evidence). "
        "Use it to resolve references in the current request, but "
        "ground factual claims in the retrieved evidence. Treat prior "
        "assistant responses as fallible.\n\n"
        + "\n\n".join(formatted)
    )
