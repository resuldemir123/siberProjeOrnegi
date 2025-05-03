import string
import hashlib
import requests

def parola_gucu_kontrol(parola):
    puan = 0
    nedenler = []

    if len(parola) >= 8:
        puan += 1
    else:
        nedenler.append("➖ Uzunluk yetersiz (min 8 karakter)")

    if any(c.islower() for c in parola) and any(c.isupper() for c in parola):
        puan += 1
    else:
        nedenler.append("➖ Büyük/küçük harf içermiyor")

    if any(c.isdigit() for c in parola) and any(c in string.punctuation for c in parola):
        puan += 1
    else:
        nedenler.append("➖ Rakam veya özel karakter içermiyor")

    try:
        with open("kelimeler.txt", "r", encoding="utf-8") as f:
            kelimeler = f.read().splitlines()
            if parola.lower() in kelimeler:
                puan -= 1
                nedenler.append("➖ Basit bir kelime içeriyor (sözlük saldırısına açık)")
    except FileNotFoundError:
        nedenler.append("⚠️ 'kelimeler.txt' bulunamadı, sözlük kontrolü atlandı.")

    return puan, nedenler

def parola_sizinti_kontrol(parola):
    sha1 = hashlib.sha1(parola.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            hashes = (line.split(":") for line in response.text.splitlines())
            for s, count in hashes:
                if s == suffix:
                    return int(count)
    except requests.RequestException:
        return -1  # Hata durumunda özel durum

    return 0
