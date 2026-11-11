import os
import tkinter as tk
import random
import threading

from gtts import gTTS
from playsound import playsound

print(os.getcwd())

SEVIYELER = {
    "A2": "a2.txt",
    "A2+": "a2plus.txt",
    "B1": "b1.txt",
    "B1+": "b1plus.txt",
    "B2": "b2.txt",
    "B2+": "b2plus.txt"
}


class Uygulama:

    def __init__(self, root):

        self.root = root
        self.root.title("Eray German Coach")
        self.root.geometry("900x550")

        self.puan = 0
        self.dogru_sayisi = 0
        self.yanlis_sayisi = 0

        self.seviye = "A2"

        self.cumleler = []

        self.almanca = ""
        self.turkce = ""

        baslik = tk.Label(
            root,
            text="ERAY GERMAN COACH",
            font=("Arial", 20, "bold")
        )
        baslik.pack(pady=10)

        self.seviye_label = tk.Label(
            root,
            text="Seviye: A2",
            font=("Arial", 14)
        )
        self.seviye_label.pack()

        self.buton_frame = tk.Frame(root)
        self.buton_frame.pack(pady=10)

        for isim in SEVIYELER:

            btn = tk.Button(
                self.buton_frame,
                text=isim,
                width=8,
                command=lambda s=isim: self.seviye_degistir(s)
            )

            btn.pack(side=tk.LEFT, padx=3)

        self.puan_label = tk.Label(
            root,
            text="Puan: 0",
            font=("Arial", 14)
        )
        self.puan_label.pack()

        self.istatistik_label = tk.Label(
            root,
            text="Doğru: 0 | Yanlış: 0 | Başarı: %0",
            font=("Arial", 12)
        )
        self.istatistik_label.pack(pady=5)

        self.cumle_label = tk.Label(
            root,
            text="",
            font=("Arial", 22),
            wraplength=800
        )
        self.cumle_label.pack(pady=20)

        self.ses_btn = tk.Button(
            root,
            text="🔊 Almanca Oku",
            font=("Arial", 12),
            command=self.cumleyi_oku
        )
        self.ses_btn.pack()

        self.giris = tk.Entry(
            root,
            font=("Arial", 16),
            width=50
        )
        self.giris.pack(pady=10)

        self.giris.bind(
            "<Return>",
            lambda event: self.kontrol()
        )

        self.kontrol_buton = tk.Button(
            root,
            text="Kontrol Et",
            font=("Arial", 12),
            command=self.kontrol
        )
        self.kontrol_buton.pack(pady=10)

        self.sonuc = tk.Label(
            root,
            text="",
            font=("Arial", 14)
        )
        self.sonuc.pack()

        self.cumleleri_yukle()
        self.yeni_soru()

    def sesi_oku(self, metin):

        def oynat():

            try:

                tts = gTTS(
                    text=metin,
                    lang="de"
                )

                dosya = "ses.mp3"

                tts.save(dosya)

                playsound(dosya)

            except Exception as hata:
                print("Ses hatası:", hata)

        threading.Thread(
            target=oynat,
            daemon=True
        ).start()

    def cumleyi_oku(self):

        if self.almanca:
            self.sesi_oku(self.almanca)

    def cumleleri_yukle(self):

        self.cumleler = []

        dosya_adi = SEVIYELER[self.seviye]

        try:

            with open(
                dosya_adi,
                "r",
                encoding="utf-8"
            ) as dosya:

                for satir in dosya:

                    satir = satir.strip()

                    if "|" in satir:

                        almanca, turkce = satir.split(
                            "|",
                            1
                        )

                        self.cumleler.append(
                            (
                                almanca,
                                turkce
                            )
                        )

        except FileNotFoundError:

            self.sonuc.config(
                text=f"{dosya_adi} bulunamadı",
                fg="red"
            )

    def seviye_degistir(self, yeni_seviye):

        self.seviye = yeni_seviye

        self.seviye_label.config(
            text=f"Seviye: {yeni_seviye}"
        )

        self.cumleleri_yukle()
        self.yeni_soru()

    def temizle(self, metin):

        metin = metin.lower().strip()

        for karakter in [
            ".", ",", "!", "?",
            ";", ":", "'", '"'
        ]:
            metin = metin.replace(
                karakter,
                ""
            )

        return metin

    def yeni_soru(self):

        if not self.cumleler:

            self.cumle_label.config(
                text="Bu seviyede veri bulunamadı."
            )

            return

        self.almanca, self.turkce = random.choice(
            self.cumleler
        )

        self.cumle_label.config(
            text=self.almanca
        )

        self.giris.delete(
            0,
            tk.END
        )

        self.sesi_oku(self.almanca)

    def istatistik_guncelle(self):

        toplam = (
            self.dogru_sayisi +
            self.yanlis_sayisi
        )

        if toplam > 0:

            basari = (
                self.dogru_sayisi /
                toplam
            ) * 100

        else:

            basari = 0

        self.istatistik_label.config(
            text=
            f"Doğru: {self.dogru_sayisi} | "
            f"Yanlış: {self.yanlis_sayisi} | "
            f"Başarı: %{basari:.1f}"
        )

    def kontrol(self):

        cevap = self.temizle(
            self.giris.get()
        )

        dogru = self.temizle(
            self.turkce
        )

        if cevap == dogru:

            self.puan += 10
            self.dogru_sayisi += 1

            self.sonuc.config(
                text="✅ Doğru",
                fg="green"
            )

        else:

            self.yanlis_sayisi += 1

            self.sonuc.config(
                text=f"❌ Doğru cevap: {self.turkce}",
                fg="red"
            )

        self.puan_label.config(
            text=f"Puan: {self.puan}"
        )

        self.istatistik_guncelle()

        self.root.after(
            1500,
            self.yeni_soru
        )


root = tk.Tk()

uygulama = Uygulama(root)

root.mainloop()
