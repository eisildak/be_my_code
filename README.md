# Be My Code - Görme Engelli Bireyler için Kod Yazma Asistan Programı

## Proje Hakkında
TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı kapsamında geliştirilen, görme engelli bireylerin Python kod yazmasını ses komutları ile sağlayan yapay zeka destekli IDE.

**Proje Sahibi:** Erol Işıldak  
**Danışman:** Öğr. Gör. Gülsüm KEMERLİ  
**Proje Ortağı:** Harun Efe Akkan  
**Kurum:** Nuh Naci Yazgan Üniversitesi

## Özellikler
- 🎤 Sesli komutlarla kod yazma
- 🔊 Coqui-XTTS v2 ile profesyonel Türkçe seslendirme
- 📁 Sol panel dosya yöneticisi
- 💻 Entegre terminal
- 🤖 AI destekli kod önerileri
- 📖 Yazılan kodları sesli okuma
- 🔗 Dosyalar arası referans sistemi

## Teknolojiler
- Python 3.8+
- PyQt5/Tkinter (GUI)
- Coqui-XTTS v2 (Text-to-Speech)
- SpeechRecognition (Ses tanıma)
- Transformers (NLP)
- OpenAI API (Kod önerileri - opsiyonel)

## Kurulum

### Otomatik Kurulum (Önerilen)
```bash
# Kurulum scriptini çalıştırılabilir yap
chmod +x install.sh

# Kurulumu başlat
./install.sh
```

### Manuel Kurulum
```bash
# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# macOS için PyAudio gereksinimleri
brew install portaudio
```

## Kullanım

### Hızlı Başlatma
```bash
# Başlatma scriptini kullan
./run.sh
```

### Manuel Başlatma
```bash
# Sanal ortamı aktif et
source venv/bin/activate

# Uygulamayı başlat
python src/main.py
```

## Sesli Komut Örnekleri
- "for döngüsü yaz"
- "while döngüsü oluştur"
- "string değişken tanımla"
- "kodu oku"
- "satır 5'i oku"
- "yeni dosya oluştur"

## 📊 Proje İstatistikleri

- **Toplam Dosya**: 25
- **Kod Satırı**: ~1,607 (sadece Python)
- **Modül Sayısı**: 6
- **Desteklenen Komut**: 12 tür
- **Sürüm**: 1.0.0

## 📚 Dokümantasyon

- 📖 [QUICKSTART.md](QUICKSTART.md) - Hızlı başlangıç kılavuzu
- 📖 [ARCHITECTURE.md](ARCHITECTURE.md) - Mimari ve teknik detaylar
- 📖 [DEVELOPER.md](DEVELOPER.md) - Geliştirici notları
- 📖 [TESTING.md](TESTING.md) - Test senaryoları
- 📖 [CHANGELOG.md](CHANGELOG.md) - Sürüm geçmişi

## 🤝 Katkıda Bulunma

Bu proje TÜBİTAK 2209-A kapsamında eğitim amaçlı geliştirilmiştir.
Sorularınız için lütfen proje danışmanı ile iletişime geçin.

## 📞 İletişim

**Proje Sahibi**: Erol Işıldak  
**Danışman**: Öğr. Gör. Gülsüm KEMERLİ  
**Proje Ortağı**: Harun Efe Akkan  
**Kurum**: Nuh Naci Yazgan Üniversitesi

## 📄 Lisans

MIT License - Eğitim amaçlı geliştirilmiştir.

---

<div align="center">

**"Teknoloji, herkes için erişilebilir olmalıdır"** 🌟

TÜBİTAK 2209-A | Nuh Naci Yazgan Üniversitesi | 2025

</div>
