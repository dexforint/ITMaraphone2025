# f9_selected_text.py
import time
import keyboard  # глобальные хоткеи
import win32clipboard  # работа с буфером Windows


def get_selected_text() -> str:
    """Копируем выделенный текст, при этом восстанавливаем старый буфер."""

    # 1. Сохраняем текущее содержимое буфера (если есть)
    win32clipboard.OpenClipboard()
    try:
        old_data = None
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            old_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()

    # 2. Имитируем Ctrl+C
    keyboard.press_and_release("ctrl+c")
    time.sleep(0.05)  # небольшой таймаут, чтобы целевое окно успело скопировать

    # 3. Читаем полученный текст
    win32clipboard.OpenClipboard()
    try:
        new_data = ""
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            new_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()

    # 4. Возвращаем старый буфер, если он отличался
    if old_data != new_data:
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            if old_data is not None:
                win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, old_data)
        finally:
            win32clipboard.CloseClipboard()

    return new_data


def on_f9():
    text = get_selected_text()
    print(f"Выделенный текст: {text!r}")


# Регистрируем хоткей F9
keyboard.add_hotkey("f9", on_f9)

print("Скрипт запущен. Выделяйте текст и жмите F9…")
keyboard.wait()  # блокировка основного потока
