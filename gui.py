import customtkinter as ctk
from tkinter import simpledialog, messagebox
from SifreAnaliz import parola_gucu_kontrol, parola_sizinti_kontrol
from caesar_cipher import caesar_sifrele, caesar_coz
from keylogger import keylogger_baslat
import threading
import string
import random
import os
import cv2  # PIL yerine OpenCV kütüphanesini import ediyoruz
import numpy as np  # OpenCV ile çalışmak için NumPy'a ihtiyacımız var

import webbrowser

# Uygulama tema ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Ana pencere
app = ctk.CTk()
app.title("🔐 Kişisel Güvenlik Testi Aracı")
app.geometry("800x700")
app.resizable(False, False)

# Tema ve renkler
renk_mavi = "#3a7ebf"
renk_kirmizi = "#bf3a3a"
renk_yesil = "#3abf5c"
renk_turuncu = "#bf7d3a"

aktif_tema = ["Dark"]

# OpenCV görüntüyü CTkImage'e dönüştürme yardımcı fonksiyonu
def cv2_to_ctkimage(cv_image, size=None):
    """OpenCV görüntüsünü CTkImage'e dönüştürür"""
    # BGR'dan RGB'ye dönüştür
    rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    
    # PIL.Image nesnesi olmadan doğrudan bir ctk.CTkImage oluştur
    if size:
        rgb_image = cv2.resize(rgb_image, size)
    
    # NumPy array'ini PhotoImage'e dönüştür
    height, width = rgb_image.shape[:2]
    from PIL import Image, ImageTk  # Sadece dönüşüm için kullanıyoruz
    
    # NumPy array'i PIL Image'e dönüştür
    pil_image = Image.fromarray(rgb_image)
    
    # CTkImage'e dönüştür
    ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(width, height))
    return ctk_image

# Tema değiştirme fonksiyonu
def temayi_degistir():
    if aktif_tema[0] == "Dark":
        ctk.set_appearance_mode("Light")
        aktif_tema[0] = "Light"
        tema_btn.configure(text="🌙 Karanlık Tema", fg_color=renk_mavi)
    else:
        ctk.set_appearance_mode("Dark")
        aktif_tema[0] = "Dark"
        tema_btn.configure(text="☀️ Açık Tema", fg_color=renk_mavi)

# 🔐 Şifre Güçlülüğü Analizi
def analiz_modulu():
    try:
        dialog = ctk.CTkInputDialog(title="Şifre Analizi", text="Lütfen şifrenizi girin:")
        parola = dialog.get_input()
        if parola:
            puan, nedenler = parola_gucu_kontrol(parola)
            sızıntı = parola_sizinti_kontrol(parola)

            analiz_sonuc = f"📊 Güç Skoru: {puan}/3\n\n"
            if nedenler:
                analiz_sonuc += "\n".join(nedenler)
            else:
                analiz_sonuc += "✅ Güçlü bir şifre!"

            sizinti_sonuc = f"\n\n🛡️ Sızıntı Kontrolü:\n{'⚠️ Bu şifre daha önce sızdırılmış!' if sızıntı > 0 else '✅ Bu şifre veritabanlarında görünmüyor.'}"

            sonuc_dialog = SonucDialog(app, "Şifre Analizi Sonucu", analiz_sonuc + sizinti_sonuc)
            app.wait_window(sonuc_dialog)
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# 🔐 Caesar Cipher Modülü
def caesar_modulu():
    try:
        caesar_pencere = ctk.CTkToplevel(app)
        caesar_pencere.title("Caesar Cipher")
        caesar_pencere.geometry("500x400")
        caesar_pencere.resizable(False, False)
        caesar_pencere.grab_set()  # Modal pencere
        
        baslik = ctk.CTkLabel(caesar_pencere, text="🔐 Caesar Cipher", font=("Segoe UI", 20, "bold"))
        baslik.pack(pady=20)
        
        # Şifreleme/Çözme seçim butonları
        secim_frame = ctk.CTkFrame(caesar_pencere, corner_radius=10)
        secim_frame.pack(pady=10, fill="x", padx=20)
        
        secim_var = ctk.StringVar(value="sifrele")
        
        sifrele_radio = ctk.CTkRadioButton(secim_frame, text="Şifrele", variable=secim_var, value="sifrele")
        sifrele_radio.pack(side="left", padx=30, pady=10)
        
        coz_radio = ctk.CTkRadioButton(secim_frame, text="Çöz", variable=secim_var, value="coz")
        coz_radio.pack(side="right", padx=30, pady=10)
        
        # Mesaj giriş alanı
        mesaj_label = ctk.CTkLabel(caesar_pencere, text="Mesajınızı girin:")
        mesaj_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        mesaj_entry = ctk.CTkTextbox(caesar_pencere, height=100, corner_radius=10)
        mesaj_entry.pack(fill="x", padx=20, pady=5)
        
        # Kaydırma değeri
        kayma_frame = ctk.CTkFrame(caesar_pencere, corner_radius=10)
        kayma_frame.pack(pady=10, fill="x", padx=20)
        
        kayma_label = ctk.CTkLabel(kayma_frame, text="Kaydırma Değeri:")
        kayma_label.pack(side="left", padx=20, pady=10)
        
        kayma_var = ctk.IntVar(value=3)
        kayma_slider = ctk.CTkSlider(kayma_frame, from_=1, to=25, variable=kayma_var, 
                                    width=200, number_of_steps=24)
        kayma_slider.pack(side="left", padx=20, pady=10)
        
        kayma_deger = ctk.CTkLabel(kayma_frame, text="3")
        kayma_deger.pack(side="left", padx=10, pady=10)
        
        # Slider değeri değişince etiketi güncelle
        def update_label(val):
            kayma_deger.configure(text=str(int(val)))
        
        kayma_slider.configure(command=update_label)
        
        # İşlem butonları
        def islem_yap():
            mesaj = mesaj_entry.get("0.0", "end").strip()
            kayma = kayma_var.get()
            secim = secim_var.get()
            
            if not mesaj:
                messagebox.showwarning("Uyarı", "Lütfen bir mesaj girin!")
                return
                
            if secim == "sifrele":
                sonuc = caesar_sifrele(mesaj, kayma)
                baslik = "🔐 Şifrelenmiş Mesaj"
            else:
                sonuc = caesar_coz(mesaj, kayma)
                baslik = "🔓 Çözülmüş Mesaj"
                
            sonuc_dialog = SonucDialog(caesar_pencere, baslik, sonuc, metin_kopyalama=True)
            caesar_pencere.wait_window(sonuc_dialog)
        
        buton_frame = ctk.CTkFrame(caesar_pencere, fg_color="transparent")
        buton_frame.pack(pady=20)
        
        iptal_btn = ctk.CTkButton(buton_frame, text="İptal", fg_color=renk_kirmizi, 
                                command=caesar_pencere.destroy, width=120)
        iptal_btn.pack(side="left", padx=10)
        
        islem_btn = ctk.CTkButton(buton_frame, text="İşlemi Gerçekleştir", fg_color=renk_yesil,
                                command=islem_yap, width=150)
        islem_btn.pack(side="left", padx=10)
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# 🕵️ Keylogger Başlat
def keylogger_modulu():
    try:
        onay = messagebox.askyesno("Keylogger", 
                            "Bu, tuş vuruşlarınızı kaydetmeye başlayacak bir eğitim simülasyonudur.\n"
                            "Gerçek bir siber güvenlik testinde kullanılmaktadır.\n\n"
                            "Devam etmek istiyor musunuz?")
        if onay:
            def baslat():
                keylogger_baslat()
                
            messagebox.showinfo("Keylogger", "Keylogger başlatıldı. input_log.txt dosyasına yazılıyor.\n"
                        "Bu simülasyonu istediğiniz zaman durdurabilirsiniz.")
            t = threading.Thread(target=baslat, daemon=True)
            t.start()
            
            # Başlatıldığını göster
            buton_durum_guncelle(btn3, "🔴 Keylogger Aktif", renk_kirmizi)
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

def buton_durum_guncelle(buton, yazi, renk):
    """Butonun yazısını ve rengini değiştirir"""
    buton.configure(text=yazi, fg_color=renk)
    # 3 saniye sonra eski haline döndür
    app.after(3000, lambda: buton.configure(text="🕵️ Keylogger Simülasyonu", fg_color=renk_mavi))

# 🔑 Güçlü Şifre Oluştur
def sifre_olustur():
    try:
        sifre_pencere = ctk.CTkToplevel(app)
        sifre_pencere.title("Güçlü Şifre Oluştur")
        sifre_pencere.geometry("500x500")
        sifre_pencere.resizable(False, False)
        sifre_pencere.grab_set()  # Modal pencere
        
        baslik = ctk.CTkLabel(sifre_pencere, text="🔑 Güçlü Şifre Oluşturucu", font=("Segoe UI", 20, "bold"))
        baslik.pack(pady=20)
        
        # Ayarlar çerçevesi
        ayarlar_frame = ctk.CTkFrame(sifre_pencere, corner_radius=10)
        ayarlar_frame.pack(pady=10, fill="x", padx=20)
        
        # Uzunluk ayarı
        uzunluk_label = ctk.CTkLabel(ayarlar_frame, text="Şifre Uzunluğu:")
        uzunluk_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        uzunluk_var = ctk.IntVar(value=16)
        uzunluk_slider = ctk.CTkSlider(ayarlar_frame, from_=6, to=64, variable=uzunluk_var, 
                                    width=300, number_of_steps=58)
        uzunluk_slider.pack(padx=20, pady=5)
        
        uzunluk_deger = ctk.CTkLabel(ayarlar_frame, text="16 karakter")
        uzunluk_deger.pack(padx=20, pady=5)
        
        # Slider değeri değişince etiketi güncelle
        def update_uzunluk(val):
            uzunluk_deger.configure(text=f"{int(val)} karakter")
        
        uzunluk_slider.configure(command=update_uzunluk)
        
        # Karakter seçenekleri
        secenekler_label = ctk.CTkLabel(ayarlar_frame, text="Karakter Seçenekleri:")
        secenekler_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        harf_var = ctk.BooleanVar(value=True)
        harf_check = ctk.CTkCheckBox(ayarlar_frame, text="Harfler (A-Z, a-z)", variable=harf_var)
        harf_check.pack(anchor="w", padx=40, pady=5)
        
        rakam_var = ctk.BooleanVar(value=True)
        rakam_check = ctk.CTkCheckBox(ayarlar_frame, text="Rakamlar (0-9)", variable=rakam_var)
        rakam_check.pack(anchor="w", padx=40, pady=5)
        
        ozel_var = ctk.BooleanVar(value=True)
        ozel_check = ctk.CTkCheckBox(ayarlar_frame, text="Özel Karakterler (!@#$%^&*)", variable=ozel_var)
        ozel_check.pack(anchor="w", padx=40, pady=5)
        
        # Şifre Oluştur
        def sifre_olustur_fonk():
            uzunluk = uzunluk_var.get()
            
            # En az bir seçeneğin seçili olduğunu kontrol et
            if not (harf_var.get() or rakam_var.get() or ozel_var.get()):
                messagebox.showwarning("Uyarı", "Lütfen en az bir karakter türü seçin!")
                return
                
            karakterler = ""
            if harf_var.get():
                karakterler += string.ascii_letters
            if rakam_var.get():
                karakterler += string.digits
            if ozel_var.get():
                karakterler += "!@#$%^&*()_+-=[]{}|;:,.<>?~"
                
            sifre = ''.join(random.choice(karakterler) for _ in range(uzunluk))
            sifre_alani.delete(0, "end")
            sifre_alani.insert(0, sifre)
        
        # Şifre alanı
        sifre_alani_label = ctk.CTkLabel(sifre_pencere, text="Oluşturulan Şifre:")
        sifre_alani_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        sifre_alani = ctk.CTkEntry(sifre_pencere, width=460, height=40, font=("Segoe UI", 14), show="")
        sifre_alani.pack(padx=20, pady=5)
        
        # Butonlar
        buton_frame = ctk.CTkFrame(sifre_pencere, fg_color="transparent")
        buton_frame.pack(pady=20)
        
        olustur_btn = ctk.CTkButton(buton_frame, text="🔄 Şifre Oluştur", fg_color=renk_mavi,
                                command=sifre_olustur_fonk, width=150)
        olustur_btn.pack(side="left", padx=10)
        
        def kopyala():
            sifre = sifre_alani.get()
            if sifre:
                app.clipboard_clear()
                app.clipboard_append(sifre)
                messagebox.showinfo("Kopyalandı", "Şifre panoya kopyalandı!")
                
        kopyala_btn = ctk.CTkButton(buton_frame, text="📋 Kopyala", fg_color=renk_yesil,
                                command=kopyala, width=120)
        kopyala_btn.pack(side="left", padx=10)
        
        kapat_btn = ctk.CTkButton(buton_frame, text="❌ Kapat", fg_color=renk_kirmizi,
                                command=sifre_pencere.destroy, width=120)
        kapat_btn.pack(side="left", padx=10)
        
        # İlk şifreyi oluştur
        sifre_olustur_fonk()
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# 📄 Logları Görüntüle
def log_goruntule():
    try:
        if os.path.exists("input_log.txt"):
            with open("input_log.txt", "r", encoding="utf-8") as f:
                icerik = f.read()
            
            log_pencere = ctk.CTkToplevel(app)
            log_pencere.title("Keylogger Logları")
            log_pencere.geometry("600x500")
            log_pencere.grab_set()  # Modal pencere
            
            baslik = ctk.CTkLabel(log_pencere, text="📄 Kayıt Edilen Tuşlar", font=("Segoe UI", 20, "bold"))
            baslik.pack(pady=20)
            
            # Log içeriği
            log_alani = ctk.CTkTextbox(log_pencere, width=560, height=350, font=("Segoe UI", 12))
            log_alani.pack(padx=20, pady=10, fill="both", expand=True)
            log_alani.insert("0.0", icerik if icerik else "⚠️ Log dosyası boş.")
            log_alani.configure(state="disabled")  # Salt okunur
            
            # Butonlar
            buton_frame = ctk.CTkFrame(log_pencere, fg_color="transparent")
            buton_frame.pack(pady=20)
            
            def kopyala():
                app.clipboard_clear()
                app.clipboard_append(icerik)
                messagebox.showinfo("Kopyalandı", "Loglar panoya kopyalandı!")
                
            kopyala_btn = ctk.CTkButton(buton_frame, text="📋 Kopyala", fg_color=renk_mavi,
                                    command=kopyala, width=120)
            kopyala_btn.pack(side="left", padx=10)
            
            temizle_btn = ctk.CTkButton(buton_frame, text="🧹 Temizle", fg_color=renk_turuncu,
                                    command=lambda: [log_temizle(), log_pencere.destroy()], width=120)
            temizle_btn.pack(side="left", padx=10)
            
            kapat_btn = ctk.CTkButton(buton_frame, text="❌ Kapat", fg_color=renk_kirmizi,
                                    command=log_pencere.destroy, width=120)
            kapat_btn.pack(side="left", padx=10)
        else:
            messagebox.showwarning("Uyarı", "Log dosyası bulunamadı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# 🧹 Logları Temizle
def log_temizle():
    try:
        if os.path.exists("input_log.txt"):
            with open("input_log.txt", "w", encoding="utf-8") as f:
                f.write("")
            messagebox.showinfo("Başarılı", "Log dosyası temizlendi.")
        else:
            messagebox.showwarning("Uyarı", "Temizlenecek log dosyası bulunamadı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# 🔍 Kamera ile Yüz Tanıma (OpenCV ile yeni özellik)
def yuz_tanima_modulu():
    try:
        # Kamera yakalama nesnesi oluştur
        kamera = cv2.VideoCapture(0)
        
        if not kamera.isOpened():
            messagebox.showerror("Hata", "Kamera açılamadı.")
            return
        
        # Yüz tanıma için Cascade sınıflandırıcısını yükle
        yuz_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Kamera görüntüsünü göstermek için yeni bir pencere oluştur
        kamera_pencere = ctk.CTkToplevel(app)
        kamera_pencere.title("Yüz Tanıma")
        kamera_pencere.geometry("640x540")
        kamera_pencere.resizable(False, False)
        kamera_pencere.grab_set()
        
        baslik = ctk.CTkLabel(kamera_pencere, text="🔍 Yüz Tanıma Simülasyonu", font=("Segoe UI", 20, "bold"))
        baslik.pack(pady=10)
        
        # Görüntü alanı
        goruntu_cerceve = ctk.CTkFrame(kamera_pencere, width=640, height=480)
        goruntu_cerceve.pack(padx=20, pady=10)
        goruntu_cerceve.pack_propagate(False)  # Boyutu sabitle
        
        # Görüntü etiketi
        goruntu_label = ctk.CTkLabel(goruntu_cerceve, text="")
        goruntu_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Durdurma flag'i
        running = [True]
        
        def kapat():
            running[0] = False
            kamera.release()
            kamera_pencere.destroy()
        
        # Kamerayı durdur butonu
        durdur_btn = ctk.CTkButton(kamera_pencere, text="❌ Kamerayı Kapat", fg_color=renk_kirmizi,
                                 command=kapat, width=150)
        durdur_btn.pack(pady=10)
        
        # Kamera görüntüsünü güncelleme fonksiyonu
        def update_goruntu():
            if running[0]:
                ret, frame = kamera.read()
                if ret:
                    # Yüz tespiti yap
                    gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    yuzler = yuz_cascade.detectMultiScale(gri, 1.3, 5)
                    
                    # Tespit edilen yüzlere dikdörtgen çiz
                    for (x, y, w, h) in yuzler:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Görüntüyü CTkImage'e dönüştür ve etiketle göster
                    ctk_img = cv2_to_ctkimage(frame, size=(600, 400))
                    goruntu_label.configure(image=ctk_img)
                    goruntu_label.image = ctk_img  # Referansı tut
                
                # Tekrar çağır
                kamera_pencere.after(10, update_goruntu)
        
        # Görüntü güncellemeyi başlat
        update_goruntu()
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# ❌ Güvenli Çıkış
def guvenli_cikis():
    if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
        app.destroy()

# OpenCV ile Görüntü İşleme Modülü (Yeni Özellik)
def goruntu_isleme_modulu():
    try:
        goruntu_pencere = ctk.CTkToplevel(app)
        goruntu_pencere.title("Görüntü İşleme")
        goruntu_pencere.geometry("700x600")
        goruntu_pencere.resizable(False, False)
        goruntu_pencere.grab_set()
        
        baslik = ctk.CTkLabel(goruntu_pencere, text="🖼️ OpenCV Görüntü İşleme", font=("Segoe UI", 20, "bold"))
        baslik.pack(pady=20)
        
        # Görüntü işleme seçenekleri
        secenekler_frame = ctk.CTkFrame(goruntu_pencere, corner_radius=10)
        secenekler_frame.pack(pady=10, fill="x", padx=20)
        
        secenekler_label = ctk.CTkLabel(secenekler_frame, text="İşleme Seçenekleri:", font=("Segoe UI", 14, "bold"))
        secenekler_label.pack(anchor="w", padx=20, pady=10)
        
        # Filtre seçim değişkeni
        filtre_var = ctk.StringVar(value="original")
        
        filtreler = [
            ("Orijinal", "original"),
            ("Gri Tonlama", "grayscale"),
            ("Bulanıklaştırma", "blur"),
            ("Kenar Algılama", "edge"),
            ("Eşikleme", "threshold")
        ]
        
        for text, value in filtreler:
            radio = ctk.CTkRadioButton(secenekler_frame, text=text, variable=filtre_var, value=value)
            radio.pack(anchor="w", padx=40, pady=5)
        
        # Görüntü alanı
        goruntu_frame = ctk.CTkFrame(goruntu_pencere, corner_radius=10)
        goruntu_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        goruntu_label = ctk.CTkLabel(goruntu_frame, text="Lütfen bir görüntü yükleyin")
        goruntu_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Butonlar
        buton_frame = ctk.CTkFrame(goruntu_pencere, fg_color="transparent")
        buton_frame.pack(pady=20)
        
        # Görüntü verisi
        goruntu_data = {"original": None, "processed": None}
        
        def dosya_yukle():
            # Dosya diyalog kutusu sistemden alıp tkinter'e geri döndüğünde görüntü yüklenebilir
            import tkinter as tk
            from tkinter import filedialog
            
            dosya = filedialog.askopenfilename(
                title="Görüntü Seç",
                filetypes=[("Görüntü Dosyaları", "*.jpg *.jpeg *.png *.bmp")]
            )
            
            if dosya:
                try:
                    # OpenCV ile görüntüyü yükle
                    goruntu = cv2.imread(dosya)
                    if goruntu is None:
                        messagebox.showerror("Hata", "Görüntü yüklenemedi.")
                        return
                    
                    # Orijinal görüntüyü sakla
                    goruntu_data["original"] = goruntu
                    
                    # Görüntüyü işle ve göster
                    filtre_uygula()
                except Exception as e:
                    messagebox.showerror("Hata", f"Görüntü işlenirken hata: {str(e)}")
        
        def filtre_uygula():
            if goruntu_data["original"] is None:
                return
            
            # Orijinal görüntünün bir kopyasını al
            goruntu = goruntu_data["original"].copy()
            
            # Seçilen filtreyi uygula
            filtre = filtre_var.get()
            if filtre == "grayscale":
                                # Gri görüntüyü tekrar BGR'ye çevir (CTkImage için)
                goruntu = cv2.cvtColor(goruntu, cv2.COLOR_GRAY2BGR)
            elif filtre == "blur":
                goruntu = cv2.GaussianBlur(goruntu, (15, 15), 0)
            elif filtre == "edge":
                gray = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (5, 5), 0)
                goruntu = cv2.Canny(gray, 50, 150)
                goruntu = cv2.cvtColor(goruntu, cv2.COLOR_GRAY2BGR)
            elif filtre == "threshold":
                gray = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
                _, goruntu = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                goruntu = cv2.cvtColor(goruntu, cv2.COLOR_GRAY2BGR)
            
            # İşlenmiş görüntüyü sakla
            goruntu_data["processed"] = goruntu
            
            # Görüntüyü göster
            ctk_img = cv2_to_ctkimage(goruntu, size=(600, 400))
            goruntu_label.configure(image=ctk_img)
            goruntu_label.image = ctk_img  # Referansı tut

        def kaydet():
            if goruntu_data["processed"] is None:
                messagebox.showwarning("Uyarı", "Önce bir görüntü işleyin!")
                return
                
            import tkinter as tk
            from tkinter import filedialog
            
            dosya = filedialog.asksaveasfilename(
                title="Görüntüyü Kaydet",
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
            )
            
            if dosya:
                try:
                    cv2.imwrite(dosya, goruntu_data["processed"])
                    messagebox.showinfo("Başarılı", "Görüntü başarıyla kaydedildi!")
                except Exception as e:
                    messagebox.showerror("Hata", f"Kayıt sırasında hata: {str(e)}")

        yukle_btn = ctk.CTkButton(buton_frame, text="📁 Görüntü Yükle", fg_color=renk_mavi,
                                command=dosya_yukle, width=150)
        yukle_btn.pack(side="left", padx=10)
        
        isle_btn = ctk.CTkButton(buton_frame, text="🔄 Filtre Uygula", fg_color=renk_yesil,
                               command=filtre_uygula, width=150)
        isle_btn.pack(side="left", padx=10)
        
        kaydet_btn = ctk.CTkButton(buton_frame, text="💾 Kaydet", fg_color=renk_turuncu,
                                 command=kaydet, width=120)
        kaydet_btn.pack(side="left", padx=10)
        
        kapat_btn = ctk.CTkButton(buton_frame, text="❌ Kapat", fg_color=renk_kirmizi,
                                command=goruntu_pencere.destroy, width=120)
        kapat_btn.pack(side="left", padx=10)
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# 🎭 Sonuç Dialog Penceresi
class SonucDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, metin_kopyalama=False, analiz_butonu=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("600x400")
        self.resizable(False, False)
        self.grab_set()  # Modal pencere

        # Başlık
        baslik = ctk.CTkLabel(self, text=title, font=("Segoe UI", 20, "bold"))
        baslik.pack(pady=20)

        # Mesaj alanı
        self.mesaj_alani = ctk.CTkTextbox(self, width=560, height=250, font=("Segoe UI", 12))
        self.mesaj_alani.pack(padx=20, pady=10)
        self.mesaj_alani.insert("0.0", message)

        if not metin_kopyalama:
            self.mesaj_alani.configure(state="disabled")  # Salt okunur

        # Butonlar
        buton_frame = ctk.CTkFrame(self, fg_color="transparent")
        buton_frame.pack(pady=20)

        if metin_kopyalama:
            kopyala_btn = ctk.CTkButton(buton_frame, text="📋 Kopyala", fg_color=renk_mavi,
                                        command=self.kopyala, width=120)
            kopyala_btn.pack(side="left", padx=10)

        if analiz_butonu:
            analiz_btn = ctk.CTkButton(buton_frame, text="🔍 Analiz Et", fg_color="orange",
                                       command=self.analiz_et, width=120)
            analiz_btn.pack(side="left", padx=10)

        tamam_btn = ctk.CTkButton(buton_frame, text="✅ Tamam", fg_color=renk_yesil,
                                  command=self.destroy, width=120)
        tamam_btn.pack(side="left", padx=10)

    def kopyala(self):
        icerik = self.mesaj_alani.get("0.0", "end")
        self.clipboard_clear()
        self.clipboard_append(icerik.strip())
        messagebox.showinfo("Kopyalandı", "Metin panoya kopyalandı!")

    def analiz_et(self):
        # Buraya analiz işlemi yapılacak fonksiyonlar eklenebilir
        messagebox.showinfo("Analiz", "Analiz işlemi başlatıldı (örnek).")

# 📌 Yardım ve Hakkında
def yardim_goster():
    messagebox.showinfo("Yardım",
        "🔐 Kişisel Güvenlik Testi Aracı\n\n"
        "Bu uygulama, temel siber güvenlik testleri yapmak için geliştirilmiştir:\n\n"
        "1. Şifre Güç Analizi - Şifrenizin ne kadar güvenli olduğunu test eder\n"
        "2. Caesar Cipher - Basit şifreleme/çözme aracı\n"
        "3. Keylogger Simülasyonu - Tuş vuruşlarını kaydeder (eğitim amaçlı)\n"
        "4. Güçlü Şifre Oluşturucu - Rastgele güçlü şifreler üretir\n"
        "5. Yüz Tanıma - OpenCV ile kamera görüntüsünde yüz tespiti\n\n"
        "⚠️ Bu araç sadece eğitim amaçlıdır. Etik kurallara uyunuz!")

def hakkinda_goster():
    messagebox.showinfo("Hakkında",
        "🔐 Kişisel Güvenlik Testi Aracı v1.0\n\n"
        "Geliştirici: Resul Demir\n"
        "Teknoloji: Python, CustomTkinter, OpenCV\n\n"
        "© 2023 Tüm hakları saklıdır.")

# 🌐 GitHub Bağlantısı
def github_ac():
    webbrowser.open("https://github.com/resuldemir/security-tool")

# 📱 Sosyal Medya Bağlantıları
def sosyal_medya(tur):
    linkler = {
        "twitter": "https://twitter.com/resuldemirtech",
        "linkedin": "https://linkedin.com/in/resuldemir",
        "website": "https://resuldemir.com"
    }
    webbrowser.open(linkler.get(tur, "https://github.com/resuldemir123"))

# 🎨 Arayüz Bileşenleri
# Başlık çerçevesi
baslik_frame = ctk.CTkFrame(app, corner_radius=10)
baslik_frame.pack(pady=20, padx=20, fill="x")

baslik = ctk.CTkLabel(baslik_frame, text="🔐 Kişisel Güvenlik Testi Aracı", 
                     font=("Segoe UI", 24, "bold"))
baslik.pack(pady=10)

# Ana butonlar çerçevesi
butonlar_frame = ctk.CTkFrame(app, corner_radius=10)
butonlar_frame.pack(pady=10, padx=20, fill="x")

# Modül butonları
btn1 = ctk.CTkButton(butonlar_frame, text="🔍 Şifre Analizi", fg_color=renk_mavi,
                    command=analiz_modulu, height=50, font=("Segoe UI", 14))
btn1.pack(pady=10, fill="x")

btn2 = ctk.CTkButton(butonlar_frame, text="🔐 Caesar Cipher", fg_color=renk_mavi,
                    command=caesar_modulu, height=50, font=("Segoe UI", 14))
btn2.pack(pady=10, fill="x")

btn3 = ctk.CTkButton(butonlar_frame, text="🕵️ Keylogger Simülasyonu", fg_color=renk_mavi,
                    command=keylogger_modulu, height=50, font=("Segoe UI", 14))
btn3.pack(pady=10, fill="x")

btn4 = ctk.CTkButton(butonlar_frame, text="🔑 Şifre Oluşturucu", fg_color=renk_mavi,
                    command=sifre_olustur, height=50, font=("Segoe UI", 14))
btn4.pack(pady=10, fill="x")

btn5 = ctk.CTkButton(butonlar_frame, text="📄 Logları Görüntüle", fg_color=renk_mavi,
                    command=log_goruntule, height=50, font=("Segoe UI", 14))
btn5.pack(pady=10, fill="x")

btn6 = ctk.CTkButton(butonlar_frame, text="🎭 Yüz Tanıma", fg_color=renk_mavi,
                    command=yuz_tanima_modulu, height=50, font=("Segoe UI", 14))
btn6.pack(pady=10, fill="x")

btn7 = ctk.CTkButton(butonlar_frame, text="🖼️ Görüntü İşleme", fg_color=renk_mavi,
                    command=goruntu_isleme_modulu, height=50, font=("Segoe UI", 14))
btn7.pack(pady=10, fill="x")

# Alt bilgi çerçevesi
alt_bilgi_frame = ctk.CTkFrame(app, corner_radius=10)
alt_bilgi_frame.pack(pady=20, padx=20, fill="x")

# Tema değiştirme butonu
tema_btn = ctk.CTkButton(alt_bilgi_frame, text="☀️ Açık Tema", fg_color=renk_mavi,
                        command=temayi_degistir, width=150)
tema_btn.pack(side="left", padx=20, pady=10)

# Yardım butonları
yardim_btn = ctk.CTkButton(alt_bilgi_frame, text="❓ Yardım", fg_color=renk_turuncu,
                          command=yardim_goster, width=100)
yardim_btn.pack(side="left", padx=10, pady=10)

hakkinda_btn = ctk.CTkButton(alt_bilgi_frame, text="ℹ️ Hakkında", fg_color=renk_turuncu,
                            command=hakkinda_goster, width=100)
hakkinda_btn.pack(side="left", padx=10, pady=10)

github_btn = ctk.CTkButton(alt_bilgi_frame, text="🐱 GitHub", fg_color="#333333",
                          command=github_ac, width=100, text_color="#ffffff")
github_btn.pack(side="left", padx=10, pady=10)

# Çıkış butonu
cikis_btn = ctk.CTkButton(alt_bilgi_frame, text="❌ Çıkış", fg_color=renk_kirmizi,
                         command=guvenli_cikis, width=100)
cikis_btn.pack(side="right", padx=20, pady=10)

# Uygulamayı başlat
app.mainloop()
                # Gri görünt