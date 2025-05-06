def caesar_sifrele(metin: str, kayma: int = 3) -> str:
    """
    Girilen metni Caesar algoritmasına göre şifreler.
    
    Args:
        metin: Şifrelenecek metin
        kayma: Alfabede kaç harf kaydırılacağını belirten değer (varsayılan: 3)
    
    Returns:
        Şifrelenmiş metin
    
    Özellikler:
        - Türkçe karakterler desteklenir
        - Büyük/küçük harf duyarlılığı korunur
        - Harf olmayan karakterler değiştirilmez
    """
    # Türkçe karakter desteği için özel karakter eşleştirmesi
    turkce_karakterler = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
    }
    
    sifreli_metin = []
    
    for karakter in metin:
        # Türkçe karakter kontrolü
        if karakter in turkce_karakterler:
            karakter = turkce_karakterler[karakter]
            
        if karakter.isalpha():
            # Büyük/küçük harf kontrolü
            base = ord('A') if karakter.isupper() else ord('a')
            # Kaydırma işlemi (mod 26 ile alfabede kalmasını sağlar)
            kaydirilmis = chr((ord(karakter) - base + kayma) % 26 + base)
            sifreli_metin.append(kaydirilmis)
        else:
            # Harf olmayan karakterler aynen korunur
            sifreli_metin.append(karakter)
    
    return ''.join(sifreli_metin)


def caesar_coz(sifreli_metin: str, kayma: int = 3) -> str:
    """
    Şifrelenmiş metni Caesar algoritmasına göre çözer.
    
    Args:
        sifreli_metin: Çözülecek şifreli metin
        kayma: Şifrelemede kullanılan kayma değeri (varsayılan: 3)
    
    Returns:
        Çözülmüş metin
    
    Not:
        Şifre çözme, ters yönde bir kaydırma işlemidir.
    """
    return caesar_sifrele(sifreli_metin, -kayma)


def caesar_frekans_analizi(metin: str) -> dict:
    """
    Metindeki karakterlerin frekans analizi.
    
    Args:
        metin: Analiz edilecek metin
    
    Returns:
        Harflerin frekans yüzdeleri sözlüğü
    """
    # Metindeki toplam harf sayısını bul
    toplam_harf_sayisi = sum(1 for karakter in metin if karakter.isalpha())
    if toplam_harf_sayisi == 0:
        return {}
    
    # Harf frekanslarını hesapla
    frekanslar = {}
    for karakter in metin:
        if karakter.isalpha():
            k = karakter.lower()
            frekanslar[k] = frekanslar.get(k, 0) + 1
    
    # Frekansları yüzdeye çevir
    for harf in frekanslar:
        frekanslar[harf] = (frekanslar[harf] / toplam_harf_sayisi) * 100
    
    return dict(sorted(frekanslar.items(), key=lambda x: x[1], reverse=True))


def caesar_automatik_coz(sifreli_metin: str, dil: str = "tr") -> dict:
    """
    Caesar şifresiyle şifrelenmiş metni otomatik çözer.
    
    Args:
        sifreli_metin: Çözülecek şifreli metin
        dil: Dil seçeneği, "tr" (Türkçe) veya "en" (İngilizce)
    
    Returns:
        Tüm olası çözümleri ve frekans analizi sonuçlarını içeren sözlük
    
    Özellikler:
        - Brute-force yöntemiyle tüm kayma değerleri denenir
        - Türkçe ve İngilizce dillerinde en sık kullanılan harfler temel alınır
        - Frekans analizi ile en olası çözüm belirlenir
    """
    # Dillere göre en sık kullanılan harfler
    en_sik_harfler = {
        "tr": ['a', 'e', 'i', 'n', 'r', 'l', 'k', 'd', 'm', 'y'],
        "en": ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd']
    }
    
    sonuclar = {}
    en_olasi_kayma = None
    en_yuksek_puan = -1
    
    # Tüm olası kayma değerlerini dene
    for kayma in range(1, 26):
        cozulen = caesar_coz(sifreli_metin, kayma)
        
        # Çözülen metnin frekans analizi
        frekanslar = caesar_frekans_analizi(cozulen)
        
        # Çözülen metnin puanını hesapla
        puan = 0
        for i, harf in enumerate(en_sik_harfler[dil][:5]):
            if harf in frekanslar:
                puan += frekanslar[harf] * (5 - i)  # İlk harfler daha önemli
        
        # Çözümü kaydet
        sonuclar[kayma] = {
            "metin": cozulen,
            "frekanslar": frekanslar,
            "puan": puan
        }
        
        # En olası çözümü güncelle
        if puan > en_yuksek_puan:
            en_yuksek_puan = puan
            en_olasi_kayma = kayma
    
    # Sonuçları düzenle
    return {
        "tum_cozumler": sonuclar,
        "en_olasi_cozum": sonuclar[en_olasi_kayma]["metin"] if en_olasi_kayma else None,
        "en_olasi_kayma": en_olasi_kayma
    }


def metni_sifrele_ve_coz(metin: str, kayma: int = 3):
    """
    Verilen metni şifreler ve ardından çözerek sonuçları gösterir.
    
    Args:
        metin: İşlenecek metin
        kayma: Kayma değeri
    """
    print(f"Orijinal metin: {metin}")
    
    # Şifreleme
    sifreli = caesar_sifrele(metin, kayma)
    print(f"\nKayma {kayma} ile şifrelenmiş: {sifreli}")
    
    # Manuel çözme
    cozulmus = caesar_coz(sifreli, kayma)
    print(f"\nManuel çözülmüş: {cozulmus}")
    
    # Otomatik çözme
    print("\nOtomatik çözme işlemi:")
    sonuclar = caesar_automatik_coz(sifreli)
    
    print(f"\nEn olası çözüm (Kayma: {sonuclar['en_olasi_kayma']}): {sonuclar['en_olasi_cozum']}")
    
    # Frekans analizi sonuçlarını göster
    print("\nEn olası çözümün frekans analizi:")
    frekanslar = sonuclar['tum_cozumler'][sonuclar['en_olasi_kayma']]['frekanslar']
    for harf, yuzde in list(frekanslar.items())[:5]:  # İlk 5 en sık harf
        print(f"{harf}: %{yuzde:.2f}")


# Kullanım örneği
if __name__ == "__main__":
    ornek_metin = "Caesar şifreleme algoritması, tarihteki en eski şifreleme yöntemlerinden biridir."
    metni_sifrele_ve_coz(ornek_metin, 7)