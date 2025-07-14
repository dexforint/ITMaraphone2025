"""
УПРАВЛЕНИЕ (цифровая клавиатура)
 Num 7  — начать запись ТОЛЬКО ВИДЕО   (MP4)
 Num 8  — начать запись ТОЛЬКО АУДИО   (MP3)
 Num 9  — начать запись ВИДЕО+АУДИО    (MP4)
 Num 5  — остановить ВСЕ текущие записи
 ESC    — выйти из приложения
"""

import subprocess
import datetime
import keyboard
import os

# ------------------------------------------------------------
# НАСТРОЙКИ
# ------------------------------------------------------------
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"  # путь к ffmpeg.exe
AUDIO_SRC = "audio=Набор микрофонов (Realtek(R) Audio)"  # название аудиоустройства
FPS = 30
PRESET = "veryfast"
AUD_QSCALE = "2"  # качество mp3: 0-5 (2 ≈ ~190-220 кбит/с VBR)

# ------------------------------------------------------------
# ПРОЦЕССЫ (будут хранить запущенный ffmpeg)
# ------------------------------------------------------------
proc_video = None  # только видео
proc_audio = None  # только аудио
proc_av = None  # видео + аудио


# ------------------------------------------------------------
# Вспомогательная функция
# ------------------------------------------------------------
def _start_ffmpeg(cmd: list[str]) -> subprocess.Popen:
    """Запустить ffmpeg с перенаправлением stdin, без консольного окна"""
    return subprocess.Popen(
        cmd, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW
    )


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _stop_proc(proc: subprocess.Popen | None, label: str):
    """Корректно остановить процесс (если он существует)"""
    if not proc or proc.poll() is not None:
        return None  # уже остановлен
    try:
        proc.stdin.write(b"q")  # корректный выход для ffmpeg
        proc.stdin.flush()
    except Exception:
        pass
    proc.wait()
    print(f"⏹️  {label} сохранён")
    return None


# ------------------------------------------------------------
# ЗАПУСК ЗАПИСЕЙ
# ------------------------------------------------------------
def start_video():
    global proc_video
    if proc_video and proc_video.poll() is None:
        print("⚠️  Видео уже пишется")
        return

    outfile = f"video_{_timestamp()}.mp4"
    cmd = [
        FFMPEG,
        "-y",
        "-f",
        "gdigrab",
        "-framerate",
        str(FPS),
        "-i",
        "desktop",
        "-c:v",
        "libx264",
        "-preset",
        PRESET,
        "-pix_fmt",
        "yuv420p",
        "-an",  # <-- отключаем аудио
        "-movflags",
        "+faststart",
        outfile,
    ]
    proc_video = _start_ffmpeg(cmd)
    print(f"🔴 Видео-запись начата  →  {outfile}")


def start_audio():
    global proc_audio
    if proc_audio and proc_audio.poll() is None:
        print("⚠️  Аудио уже пишется")
        return

    outfile = f"audio_{_timestamp()}.mp3"
    cmd = [
        FFMPEG,
        "-y",
        "-f",
        "dshow",
        "-i",
        AUDIO_SRC,
        "-c:a",
        "libmp3lame",
        "-qscale:a",
        AUD_QSCALE,
        outfile,
    ]
    proc_audio = _start_ffmpeg(cmd)
    print(f"🔴 Аудио-запись начата  →  {outfile}")


def start_av():
    global proc_av
    if proc_av and proc_av.poll() is None:
        print("⚠️  Видео+аудио уже пишутся")
        return

    outfile = f"av_{_timestamp()}.mp4"
    cmd = [
        FFMPEG,
        "-y",
        "-f",
        "gdigrab",
        "-framerate",
        str(FPS),
        "-i",
        "desktop",
        "-f",
        "dshow",
        "-i",
        AUDIO_SRC,
        "-c:v",
        "libx264",
        "-preset",
        PRESET,
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        outfile,
    ]
    proc_av = _start_ffmpeg(cmd)
    print(f"🔴 Видео+аудио-запись начата  →  {outfile}")


# ------------------------------------------------------------
# ОСТАНОВКА ВСЕХ
# ------------------------------------------------------------
def stop_all():
    global proc_video, proc_audio, proc_av
    any_running = any(p and p.poll() is None for p in (proc_video, proc_audio, proc_av))
    if not any_running:
        print("ℹ️  Сейчас ничего не пишется")
        return

    proc_video = _stop_proc(proc_video, "Видео")
    proc_audio = _stop_proc(proc_audio, "Аудио")
    proc_av = _stop_proc(proc_av, "Видео+Аудио")


# ------------------------------------------------------------
# ГОРЯЧИЕ КЛАВИШИ
# ------------------------------------------------------------
def main():
    print("Numpad:  1-видео  2-аудио  3-видео+аудио  5-стоп  |  ESC-выход")
    keyboard.add_hotkey("num 1", start_video)
    keyboard.add_hotkey("num 2", start_audio)
    keyboard.add_hotkey("num 3", start_av)
    keyboard.add_hotkey("num 5", stop_all)

    # ждём, пока пользователь нажмёт Esc
    keyboard.wait("esc")
    # при выходе останавливаем всё на всякий случай
    stop_all()


if __name__ == "__main__":
    main()
