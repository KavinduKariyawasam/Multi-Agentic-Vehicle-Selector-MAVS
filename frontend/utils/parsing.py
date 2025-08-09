# frontend/utils/parsing.py
import json
import re
from typing import Any, Dict, Optional

# Match ```json { ... } ``` OR ``` { ... } ```
FENCE_RE = re.compile(r"```(?:json)?\s*({.*?})\s*```", re.DOTALL | re.IGNORECASE)

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    if not isinstance(text, str):
        return None

    # Prefer the LAST fenced block (LLMs often put the “final” at the end)
    blocks = FENCE_RE.findall(text)
    for candidate in reversed(blocks):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Fallback: biggest {...} slice
    first, last = text.find("{"), text.rfind("}")
    if first != -1 and last != -1 and last > first:
        candidate = text[first:last+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None
    return None

def extract_structured_result(result: Any) -> Optional[Dict[str, Any]]:
    # Already structured?
    if isinstance(result, dict) and "top_picks" in result:
        return result

    # Your shape: result is a dict with a markdown blob under "raw"
    if isinstance(result, dict) and "raw" in result:
        return extract_json_from_text(result["raw"])

    # Or a raw markdown string
    if isinstance(result, str):
        return extract_json_from_text(result)

    return None
