# Be My Code - Sesli Python IDE

🎤 **Görme Engelli Bireyler için Kod Yazma Asistanı**

## 📚 Proje Bilgileri

- **TÜBİTAK 2209-A Projesi**
- **Proje Sahibi:** Erol Işıldak
- **Danışman:** Öğr. Gör. Gülsüm KEMERLİ
- **Proje Ortağı:** Harun Efe Akkan

## ✨ Özellikler

### 🎤 Sesli Komutlar
- Web Speech API ile Türkçe ses tanıma
- Text-to-Speech ile sesli geri bildirim
- Klavye kısayolu: `Ctrl+M` veya `Cmd+M`

### 🤖 Gemini AI Entegrasyonu
- Doğal dil ile Python kod üretme
- Context-aware akıllı öneriler
- Türkçe komut desteği

### 💻 IDE Özellikleri
- CodeMirror kod editörü (syntax highlighting)
- Terminal çıktı görüntüleme
- Dosya yönetimi (kaydet/yükle)
- **F5** ile kod çalıştırma
- **Ctrl+S** ile dosya kaydetme

### 🎯 Hızlı Komutlar
1. **Birinci komut:** Alt satıra geç
2. **İkinci komut:** Kodu çalıştır
3. **Üçüncü komut:** 1. satırı oku
4. **Dördüncü komut:** Terminal çıktısını oku
5. **Beşinci komut:** Komut listesini oku

## 🚀 Kurulum

### 1. Gereksinimler
- Python 3.9+
- pip (Python package manager)

### 2. Proje Kurulumu

```bash
# Repository'yi klonlayın
git clone https://github.com/eisildak/be_my_code.git
cd be_my_code

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktifleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Gemini API Key Ayarlama

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'dan API key alın
2. `.env` dosyası oluşturun:

```bash
# .env dosyasına ekleyin
GEMINI_API_KEY=your_api_key_here
```

## 🌐 Çalıştırma

### Web IDE (Önerilen)

```bash
# Flask sunucusunu başlatın
python app.py

# Tarayıcınızda açın:
# http://localhost:5001
```

**Not:** Mikrofon erişimi için modern bir tarayıcı (Chrome, Edge, Safari) gereklidir.

### Masaüstü IDE (PyQt5)

```bash
# PyQt5 uygulamasını başlatın
python src/main.py
```

## 🎨 Tema Renkleri

- **Ana Koyu:** #1A181B
- **Altın Sarısı:** #D7BB56 (vurgu)
- **Mor:** #9F8DCE (secondary)
- **Açık Gri:** #EEECEE (text/background)

## 📖 Kullanım

### Sesli Komut Örnekleri

**Temel Komutlar:**
- "isim değişkeni oluştur"
- "1'den 10'a kadar yazdır"
- "kullanıcıdan yaş al"
- "faktöriyel fonksiyonu yaz"

**Dikteye Geçme:**
- Tanınmayan komutlar otomatik olarak metne dönüştürülür

### Klavye Kısayolları

- **Ctrl+M / Cmd+M:** Mikrofonu aç/kapat
- **F5:** Kodu çalıştır
- **Ctrl+S / Cmd+S:** Dosyayı kaydet
- **Ctrl+/ / Cmd+/:** Satırı yorum yap

## 🛠️ Teknolojiler

### Backend
- Flask (Web framework)
- Flask-SocketIO (WebSocket desteği)
- Google Generative AI (Gemini)
- Jedi (Python kod analizi)

### Frontend
- HTML5
- CSS3 (Custom design)
- JavaScript (ES6+)
- CodeMirror (Kod editörü)
- Web Speech API (Ses tanıma/TTS)
- Socket.IO (Gerçek zamanlı iletişim)

### Desktop
- PyQt5 (GUI framework)
- pyttsx3 (Offline TTS)
- SpeechRecognition (Google Speech API)

## 📁 Proje Yapısı

```
be_my_code/
├── app.py                  # Flask web uygulaması
├── src/
│   ├── main.py            # PyQt5 masaüstü uygulaması
│   ├── modules/           # Python modülleri
│   │   ├── gemini_code_generator.py
│   │   ├── nlp_processor.py
│   │   ├── speech_recognizer.py
│   │   └── text_to_speech_alt.py
│   └── ui/                # PyQt5 arayüzleri
├── templates/             # HTML şablonları
│   └── index.html
├── static/                # CSS, JavaScript
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── editor.js
│       ├── voice.js
│       └── tts.js
└── requirements.txt       # Python bağımlılıkları
```

## 🤝 Katkıda Bulunma

Bu proje TÜBİTAK 2209-A araştırma projesidir. Önerileriniz için issue açabilirsiniz.

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **Proje Sahibi:** Erol Işıldak
- **Danışman:** Öğr. Gör. Gülsüm KEMERLİ
- **Proje Ortağı:** Harun Efe Akkan

## 🙏 Teşekkürler

Bu proje, görme engelli bireylerin programlama öğrenmesini kolaylaştırmak amacıyla geliştirilmiştir. TÜBİTAK 2209-A programına destekleri için teşekkür ederiz.

---

**🎤 Be My Code** - Ses ile kod yazmanın gücünü keşfedin!
