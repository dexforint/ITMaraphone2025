import keyboard
from typing import Callable


def llm_query() -> None:
    # ensure_ascii=True encoding='utf-8'

    path = "logs.md"

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    string_messages = text.split("=====")  # !!
    string_messages = [message.strip() for message in string_messages]
    if len(string_messages) == 0:
        print("No queries!")
        return

    messages = []
    for i, string_message in enumerate(string_messages):
        if i == 0:
            role = "system"
        elif i % 2 == 0:
            role = "user"
        else:
            role = "assistant"

        messages.append({"role": role, "content": string_message})


button2func: dict[str, Callable[[], None]] = {
    "F8": llm_query,
}


def main() -> None:
    for button, func in button2func.items():
        print(button, "->", func.__name__)
        keyboard.add_hotkey(button, func)
    keyboard.wait("F12")  # блокировка до ESC


if __name__ == "__main__":
    main()
