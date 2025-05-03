# main.py
from sifre_analiz import parola_gucu_kontrol, parola_sizinti_kontrol
from caesar_cipher import caesar_sifrele, caesar_coz
from keylogger import keylogger_baslat

def menu():
    while True:
        print("\n🔐 Kişisel Güvenlik Testi Aracı")
        print("1 - Şifre Güçlülüğü Analizi")
        print("2 - Caesar Cipher Şifrele/Çöz")
        print("3 - Keylogger Simülasyonu")
        print("4 - Çıkış")

        secim = input("Seçiminiz: ")

        if secim == "1":
            parola = input("Şifrenizi girin: ")
            puan, nedenler = parola_gucu_kontrol(parola)
            sizinti_sayisi = parola_sizinti_kontrol(parola)

            print("\n🔍 Analiz Sonucu:")
            if puan >= 3:
                print("✅ Şifreniz güçlü.")
            elif puan == 2:
                print("⚠ Orta seviye şifre.")
            else:
                print("❌ Şifreniz zayıf.")

            for neden in nedenler:
                print(neden)

            if sizinti_sayisi > 0:
                print(f"⚠ Bu şifre daha önce {sizinti_sayisi} kez sızdırılmış!")
            else:
                print("✅ Şifreniz sızdırılmış değil.")

        elif secim == "2":
            metin = input("Metni girin: ")
            kayma = int(input("Kayma değeri (varsayılan 3): ") or 3)
            sifreli = caesar_sifrele(metin, kayma)
            print(f"🔐 Şifrelenmiş: {sifreli}")
            print(f"🔓 Çözülmüş: {caesar_coz(sifreli, kayma)}")

        elif secim == "3":
            keylogger_baslat()

        elif secim == "4":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

if __name__ == "__main__":
    menu()
