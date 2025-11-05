import json
import re

INPUT_FILE = "conversa_chat_5"

def parse_sse(stream_text):
    blocks = re.split(r'\n\n+', stream_text.strip())
    tokens = []
    for block in blocks:
        lines = block.strip().splitlines()
        event = None
        data_json = None
        for line in lines:
            if line.startswith("event:"):
                event = line.split("event:", 1)[1].strip()
            elif line.startswith("data:"):
                data_json = line.split("data:", 1)[1].strip()
        if event == "delta" and data_json:
            try:
                data = json.loads(data_json)
            except json.JSONDecodeError:
                continue
            for change in data.get("v", []):
                if not isinstance(change, dict):
                    continue
                path = change.get("p", "")
                value = change.get("v", "")
                if path.startswith("/message/content/parts/0") and isinstance(value, str):
                    tokens.append(value)
    return "".join(tokens)

if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw = f.read()

    full_text = parse_sse(raw)
    print(full_text)
