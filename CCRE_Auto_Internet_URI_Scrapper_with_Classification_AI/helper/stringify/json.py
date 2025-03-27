import json

def stringify_to_json(data):
    try:
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    except (TypeError, ValueError) as e:
        raise ValueError(f"Unable to stringify data: {e}")
