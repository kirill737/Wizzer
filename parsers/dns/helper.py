import json
DEBUG_MODE = 1
STEP_MODE = 1
DNS_URL = "https://www.dns-shop.ru"

def debug_print(text: str) -> None:
    if DEBUG_MODE:
        print(text)
def step_print(text: str) -> None:
    if STEP_MODE:
        print(text)

def save_log_file(path: str, content: json) -> None:
    if DEBUG_MODE:
        debug_print(f"Saving {path}")
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

def save_json(path: str, content: json) -> None:
    debug_print(f"Saving {path}")
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)