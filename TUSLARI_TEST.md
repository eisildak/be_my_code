# Be My Code - Tuş Kombinasyonları Test Rehberi

## ✅ Düzeltildi: F5 Tuşu Artık ÇALIŞTIRIR

### 🔧 Yapılan Değişiklikler:
1. **F5 tuşu açıkça tanımlandı**: `Qt.Key_F5` ile doğrudan bağlandı
2. **keyPressEvent eklendi**: Tüm tuş kombinasyonları merkezi bir yerden yönetiliyor
3. **Toolbar buton metni güncellendi**: "▶️ ÇALIŞTIRUN (F5)" daha görünür

---

## 🎹 Tüm Kısayollar

### Kod Çalıştırma
- **F5** → Kodu çalıştırır (print çıktıları terminalde görünür)

### Ses Komutları  
- **Ctrl+M** → Ses komutunu dinle ("Dinliyorum, buyrun" der)

### Kod Okuma
- **Ctrl+R** → Tüm kodu sesli oku
- **Ctrl+L** → Bulunduğun satırı oku

### Kod Önerileri
- **Ctrl+Space** → Kod önerileri al

### Dosya İşlemleri
- **Ctrl+N** → Yeni dosya
- **Ctrl+O** → Dosya aç
- **Ctrl+S** → Kaydet
- **Ctrl+Q** → Çıkış

---

## 🧪 Test Senaryosu

### 1. F5 Tuşunu Test Et
```python
# Editöre şu kodu yaz:
print("Merhaba Dünya")
isim = "Harun Efe Akkan"
print(f"İsim: {isim}")

# F5'e bas - Terminal panelinde şunları göreceksin:
# >>> Kod çalıştırılıyor...
# Merhaba Dünya
# İsim: Harun Efe Akkan
# ✅ Kod başarıyla çalıştırıldı
```

### 2. Ses Komutunu Test Et
1. **Ctrl+M** tuşuna bas
2. "Dinliyorum, buyrun" sesini duy
3. Terminalde `🎤 MİKROFON DİNLİYOR` yazısını gör
4. Şunu söyle: **"isim adında string değişken oluştur değeri ahmet olsun"**
5. Editörde kod oluşsun: `isim = "ahmet"`

### 3. Kod Okumayı Test Et
1. Editörde birkaç satır kod yaz
2. **Ctrl+R** tuşuna bas → Tüm kodu okur
3. **Ctrl+L** tuşuna bas → Bulunduğun satırı okur

---

## 🐛 Sorun Giderme

### F5 Çalışmıyorsa:
1. Editör alanına odaklan (editöre tıkla)
2. Kod yaz
3. Tekrar F5'e bas
4. Terminal paneline bak - çıktılar orada görünür

### Ses Komutları Çalışmıyorsa:
1. macOS'ta **Sistem Ayarları → Gizlilik ve Güvenlik → Mikrofon**
2. Terminal veya Python'a mikrofon izni ver
3. Uygulamayı yeniden başlat

### Kod Çıktıları Görünmüyorsa:
1. Terminal panelini kontrol et (sağ altta)
2. `print()` fonksiyonunu kullandığından emin ol
3. Hata varsa terminalde kırmızı yazıyla gösterilir

---

## 📊 Beklenen Davranışlar

| Tuş | Durum | Ses Geri Bildirimi | Terminal Çıktısı |
|-----|-------|-------------------|------------------|
| F5 | Kod var | "Kod çalıştırılıyor" → "Kod başarıyla çalıştırıldı" | print() çıktıları görünür |
| F5 | Kod yok | "Çalıştırılacak kod yok" | ❌ Editörde kod bulunmuyor |
| Ctrl+M | Mikrofon izni var | "Dinliyorum, buyrun" | 🎤 MİKROFON DİNLİYOR |
| Ctrl+R | Kod var | Kodu okur | - |
| Ctrl+L | Satır var | Satırı okur | - |

---

## ✨ Yeni Özellikler

1. **stdout yönlendirme**: print() çıktıları artık terminalde görünür
2. **Detaylı hata mesajları**: Kod hataları terminalde gösterilir
3. **Ses feedback**: Her işlem için sesli geri bildirim
4. **Debug mesajları**: Terminal çıktısında 🎤, 🔍, ✅ gibi emoji'ler

---

**Not**: Uygulamayı test ettikten sonra Harun Efe Akkan ile birlikte gerçek kullanım senaryolarını deneyin!
