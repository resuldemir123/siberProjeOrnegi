def caesar_sifrele(metin: str, kayma: int = 3) -> str:
    """
    Girilen metni Caesar algoritmasına göre şifreler.
    Sadece harfler kaydırılır, diğer karakterler aynen kalır.
    """
    sifreli_metin = []

    for karakter in metin:
        if karakter.isalpha():
            base = ord('A') if karakter.isupper() else ord('a')
            kaydirilmis = chr((ord(karakter) - base + kayma) % 26 + base)
            sifreli_metin.append(kaydirilmis)
        else:
            sifreli_metin.append(karakter)

    return ''.join(sifreli_metin)

def caesar_coz(sifreli_metin: str, kayma: int = 3) -> str:
    """
    Şifrelenmiş metni Caesar algoritmasına göre çözer.
    """
    return caesar_sifrele(sifreli_metin, -kayma)

def caesar_automatik_coz(sifreli_metin: str) -> str:
    """
    Caesar şifresiyle şifrelenmiş metni otomatik çözer. 
    Brute-force yöntemiyle her kayma değeri için çözüm dener.
    Anlamlı bir çözüm bulunduğunda döner.
    """
    for kayma in range(1, 26):
        cozulen = caesar_coz(sifreli_metin, kayma)
        print(f"Kayma {kayma}: {cozulen}")
        
        # Anlamlı metin kontrolü (harf dışındaki karakterler göz ardı edilir)
        if all(karakter.isalpha() or karakter.isspace() for karakter in cozulen):
            return f"Çözüm bulundu (Kayma: {kayma}): {cozulen}"
    
    return "Brute-force ile çözüm bulunamadı."

