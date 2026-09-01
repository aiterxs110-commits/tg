import json
import os
from typing import Dict, List
from config import DEFAULT_START_MESSAGE

DATA_FILE = "data/config.json"

DEFAULT_DATA = {
    "start_message": DEFAULT_START_MESSAGE,
    "buttons": [
        {"text": "📮 我要投稿", "type": "callback", "value": "请直接发送你要投稿的图文消息"}
    ],
    "custom_commands": {}
}

def _load_data() -> Dict:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=2)
        return DEFAULT_DATA.copy()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_data(data: Dict):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_start_message() -> str:
    return _load_data().get("start_message", DEFAULT_START_MESSAGE)

def set_start_message(text: str):
    data = _load_data()
    data["start_message"] = text
    _save_data(data)

def get_buttons() -> List[Dict]:
    return _load_data().get("buttons", DEFAULT_DATA["buttons"])

def add_button(text: str, btn_type: str, value: str) -> bool:
    data = _load_data()
    for btn in data["buttons"]:
        if btn["text"] == text:
            return False
    data["buttons"].append({
        "text": text,
        "type": btn_type,
        "value": value
    })
    _save_data(data)
    return True

def delete_button(text: str) -> bool:
    data = _load_data()
    original_len = len(data["buttons"])
    data["buttons"] = [b for b in data["buttons"] if b["text"] != text]
    if len(data["buttons"]) < original_len:
        _save_data(data)
        return True
    return False

def clear_buttons() -> bool:
    data = _load_data()
    data["buttons"] = []
    _save_data(data)
    return True

def get_custom_commands() -> Dict:
    return _load_data().get("custom_commands", {})

def add_custom_command(cmd_name: str, reply_text: str) -> bool:
    data = _load_data()
    if cmd_name in data.get("custom_commands", {}):
        return False
    if "custom_commands" not in data:
        data["custom_commands"] = {}
    data["custom_commands"][cmd_name] = reply_text
    _save_data(data)
    return True

def delete_custom_command(cmd_name: str) -> bool:
    data = _load_data()
    if cmd_name not in data.get("custom_commands", {}):
        return False
    del data["custom_commands"][cmd_name]
    _save_data(data)
    return True
