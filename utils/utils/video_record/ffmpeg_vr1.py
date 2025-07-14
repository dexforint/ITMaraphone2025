"""
F8  – старт записи
F9  – стоп
ESC – выход
"""

import subprocess
import datetime
import keyboard
import os

# ------------------------------------------------------------------
# Настройки
# ------------------------------------------------------------------
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"  # путь к ffmpeg.exe
AUDIO_SRC = "audio=Набор микрофонов (Realtek(R) Audio)"  # имя аудиоустройства
FPS = 30  # кадры/с
BITRATE_A = "128k"
PRESET = "veryfast"  # x264-пресет
# ------------------------------------------------------------------

rec_proc = None  # сюда положим запущенный FFmpeg-процесс


def start_recording() -> None:
    """Запустить ffmpeg, писать экран+звук в mp4"""
    global rec_proc
    if rec_proc:
        print("⚠️  Запись уже идёт")
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"record_{ts}.mp4"

    cmd = [
        FFMPEG,
        "-y",
        # видео: весь Desktop через GDI
        "-f",
        "gdigrab",
        "-framerate",
        str(FPS),
        "-i",
        "desktop",
        # аудио: выбранное устройство DirectShow
        "-f",
        "dshow",
        "-i",
        AUDIO_SRC,
        # кодирование
        "-c:v",
        "libx264",
        "-preset",
        PRESET,
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        BITRATE_A,
        # для более быстрой отдачи файла + корректные атомы
        "-movflags",
        "+faststart",
        outfile,
    ]

    # stdin=PIPE — чтобы потом послать «q» и красиво закрыться
    rec_proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW
    )
    print(f"🔴 Запись начата → {outfile}")


def stop_recording() -> None:
    """Остановить запись, корректно завершив mp4"""
    global rec_proc
    if not rec_proc:
        print("⚠️  Сейчас ничего не пишется")
        return

    # Отправляем 'q' — FFmpeg завершает и дописывает атомы MP4
    try:
        rec_proc.stdin.write(b"q")
        rec_proc.stdin.flush()
    except Exception:
        pass

    rec_proc.wait()  # ждём, пока файл закроется
    rec_proc = None
    print("⏹️  Запись остановлена")


def main() -> None:
    print("Hotkeys:  F8-start   F9-stop   Esc-exit")
    keyboard.add_hotkey("F8", start_recording)
    keyboard.add_hotkey("F9", stop_recording)
    keyboard.wait("esc")  # блокировка до ESC


if __name__ == "__main__":
    main()
