

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from urunGui import *

app = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()


#Veritabanı İşlemleri

import sqlite3
baglanti = sqlite3.connect("urunler.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute("CREATE TABLE IF NOT EXISTS urun(urunKodu INT,urunAdi TEXT,birimFiyat INT,stokMiktari INT,urunAciklaması TEXT,marka TEXT,kategori TEXT)")
baglanti.commit()

def kayit_ekle():
    urunKodu = int(ui.lneUrunKodu.text())
    urunAdi = ui.lneUrunAdi.text()
    birimFiyat = int(ui.lneBirimFiyat.text())
    stokMiktarı = int(ui.lneStokMiktari.text())
    urunAciklamasi = ui.lneUrunAciklamasi.text()
    marka = ui.cmbMarka.currentText()
    kategori = ui.cmbKategori.currentText() 

    try:
        ekle = "insert into urun(urunKodu,urunAdi,birimFiyat,stokMiktari,urunAciklaması,marka,kategori) values (?,?,?,?,?,?,?)"
        islem.execute(ekle,(urunKodu,urunAdi,birimFiyat,stokMiktarı,urunAciklamasi,marka,kategori))
        baglanti.commit()
        kayıt_listele()
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı",10000)
    except Exception as error:
        ui.statusbar.showMessage("Kayıt Eklenemedi.\nHata Çıktısı ==" + str(error),3000)


def kayıt_listele():
    ui.tblTabloListele.clear()
    ui.tblTabloListele.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adı","Birim Fiyatı","Stok Miktarı","Ürün Açıklama","Markası","Kategori"))
    ui.tblTabloListele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgu = "SELECT * FROM urun"
    islem.execute(sorgu)
    
    for indexSatir,kayitNumamrasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumamrasi):
            ui.tblTabloListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

def kategoriyi_listele():
    listelenecek_kategori = ui.cmbKategoriListele.currentText()
    sorgu = "SELECT * FROM urun where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tblTabloListele.clear()
    for indexSatir,kayitNumamrasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumamrasi):
            ui.tblTabloListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

def kayıt_sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Mesajı","Silmek İstediğinizden Eminmisiniz ?",QMessageBox.Yes | QMessageBox.No)
    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tblTabloListele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()
        sorgu = "DELETE FROM urun where urunKodu = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi.",5000)
            kayıt_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Meydana Geldi =="+ str(error),3000)
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi.")

def kayıt_güncelle():
    güncelle_mesaj = QMessageBox.question(pencere,"Güncelleme Onayı","Bu Kaydı Güncellemek İstediğinize Eminmisiniz? ",QMessageBox.Yes | QMessageBox.No)
    if güncelle_mesaj == QMessageBox.Yes:
        try:
            urunKodu = ui.lneUrunKodu.text()
            urunAdi = ui.lneUrunAdi.text()
            birimFiyat = ui.lneBirimFiyat.text()
            stokMiktarı = ui.lneStokMiktari.text()
            urunAciklamasi = ui.lneUrunAciklamasi.text()
            marka = ui.cmbMarka.currentText()
            kategori = ui.cmbKategori.currentText()

            if urunAdi == "" and birimFiyat == "" and stokMiktarı == "" and urunAciklamasi == "" and marka == "":
                islem.execute("update urun set kategori = ? where urunKodu = ?",(kategori,urunKodu))

            elif urunAdi == "" and birimFiyat == "" and stokMiktarı == "" and urunAciklamasi == "" and kategori == "":
                islem.execute("update urun set marka = ? where urunKodu = ?",(marka,urunKodu))

            elif urunAdi == "" and birimFiyat == "" and stokMiktarı == ""  and marka == "" and kategori == "":
                islem.execute("update urun set urunAciklamasi = ? where urunKodu = ?",(urunAciklamasi,urunKodu))
            
            elif urunAdi == "" and birimFiyat == "" and urunAciklamasi == "" and marka == "" and kategori == "":
                islem.execute("update urun set stokMiktari = ? where urunKodu = ?",(stokMiktarı,urunKodu))

            elif urunAdi == "" and stokMiktarı == "" and urunAciklamasi == "" and marka == "":
                islem.execute("update urun set birimFiyat = ? where urunKodu = ?",(birimFiyat,urunKodu))

            elif birimFiyat == "" and stokMiktarı == "" and urunAciklamasi == "" and marka == "":
                islem.execute("update urun set urunAdi = ? where urunKodu = ?",(urunAdi,urunKodu))


            else:
                islem.execute("update urun set urunAdi = ?, birimFiyat = ?, stokMiktari = ?,urunAciklaması = ?, marka = ?, kategori = ? where urunKodu = ?",
                (urunAdi,birimFiyat,stokMiktarı,urunAciklamasi,marka,kategori,urunKodu))
            baglanti.commit()
            kayıt_listele()
            ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi",5000)
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı =="+str(error),3000)
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi",3000)





# Butonlar

ui.btnEkle.clicked.connect(kayit_ekle)
ui.btnListeleme.clicked.connect(kayıt_listele)
ui.btnKategoriyeGoreListele.clicked.connect(kategoriyi_listele)
ui.btnSil.clicked.connect(kayıt_sil)
ui.btnGuncelleme.clicked.connect(kayıt_güncelle)


sys.exit(app.exec_())