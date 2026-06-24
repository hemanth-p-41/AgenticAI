import json
import re
from typing import Any


def safe_json_parser(text: str) -> Any:
    """Attempt to extract and parse JSON from `text`.

    Handles common cases where the model returns JSON inside markdown code fences
    or returns trailing text. Raises ValueError if parsing fails.
    """
    if not text:
        raise ValueError("Empty response")

    # Remove markdown code fences
    code_fence_re = re.compile(r"```(?:json)?\n?(.*?)```", re.DOTALL)
    m = code_fence_re.search(text)
    if m:
        text = m.group(1).strip()

    # Sometimes models return content after or before JSON — try to find first { or [
    first_brace = min((text.find(c) for c in ('{', '[') if text.find(c) != -1), default=-1)
    if first_brace > 0:
        text = text[first_brace:]

    # Remove trailing backticks or stray markdown
    text = text.strip().rstrip('`')

    # Try to fix common issues: single quotes -> double quotes for keys/strings
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # last-ditch attempt: replace single quotes with double quotes
        try:
            fixed = text.replace("'", '"')
            return json.loads(fixed)
        except Exception as e:
            raise ValueError(f"Could not parse JSON: {e}\nOriginal: {text}")
