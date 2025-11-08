# 🎤 Be My Code - Sesli Python IDE

**Görme Engelli Bireyler İçin Kod Yazma Asistanı**

## 📚 Proje Bilgileri

Bu proje, **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında geliştirilmiştir.

- **Proje Sahibi:** Erol Işıldak
- **Danışman:** Öğr. Gör. Gülsüm KEMERLİ
- **Proje Ortağı:** Harun Efe Akkan
- **Kurum:** Nuh Naci Yazgan Üniversitesi

## 🎯 Proje Amacı

Görme engelli bireylerin Python programlama dilini öğrenmesini ve kod yazmalarını kolaylaştırmak için sesli komutlar ve yapay zeka destekli bir IDE geliştirmek.

## ✨ Özellikler

### � Sesli Komutlar
- **Web Speech API** ile Türkçe ses tanıma
- **Gemini TTS** ile sesli geri bildirim
- Klavye kısayolu: `Ctrl+M` veya `Cmd+M`
- Ara sonuçları canlı görüntüleme

### 🤖 Gemini AI Entegrasyonu
- Doğal dil ile Python kod üretme
- Context-aware akıllı öneriler
- Türkçe komut desteği
- Gemini 2.5 Flash model kullanımı

### 💻 IDE Özellikleri
- **CodeMirror** kod editörü (syntax highlighting)
- Monokai dark theme
- Terminal çıktı görüntüleme
- **F5** ile kod çalıştırma (simülasyon)
- **Ctrl+R** ile kodu sesli okuma
- Responsive tasarım (mobil uyumlu)

### 🎨 Erişilebilirlik
- Yüksek kontrast renk paleti
- Büyük font boyutları (16px+)
- Klavye odaklı navigasyon
- ARIA etiketleri
- Sesli geri bildirim sistemi

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Modern web tarayıcısı (Chrome, Edge, Safari önerilir)
- İnternet bağlantısı (API çağrıları için)
- Mikrofon (sesli komutlar için)

### Kurulum

1. **Repository'yi klonlayın**
```bash
git clone https://github.com/eisildak/be_my_code.git
cd be_my_code
```

2. **Gemini API Key alın**
   - [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
   - "Create API Key" butonuna tıklayın
   - API anahtarınızı kopyalayın

3. **API Anahtarını yapılandırın**
   - `index.html` dosyasını açın
   - Satır 292'de `GEMINI_API_KEY` değerini güncelleyin:
   ```javascript
   GEMINI_API_KEY: "YOUR_API_KEY_HERE",
   ```

4. **Uygulamayı çalıştırın**
```bash
# Python ile basit HTTP sunucu
python3 -m http.server 8000

# Veya Node.js varsa
npx http-server -p 8000
```

5. **Tarayıcınızda açın**
   - http://localhost:8000

### GitHub Pages Üzerinden Kullanım

Proje GitHub Pages'de yayında: 
**https://eisildak.github.io/be_my_code/**

## 📖 Kullanım Kılavuzu

### Sesli Komut Örnekleri

#### Temel Yapılar
- `"for döngüsü yaz"`
- `"while döngüsü oluştur"`
- `"if else koşulu yaz"`
- `"string değişken tanımla isim"`
- `"print fonksiyonu yaz Merhaba Dünya"`

#### Özel Komutlar
- `"kodu sesli oku"` - Editördeki kodu okur
- `"kodu çalıştır"` - Kodu simüle eder

### Klavye Kısayolları

| Kısayol | Fonksiyon |
|---------|-----------|
| `Ctrl+M` / `Cmd+M` | Mikrofonu aç/kapat |
| `F5` | Kodu çalıştır |
| `Ctrl+R` / `Cmd+R` | Kodu sesli oku |

### Hızlı Komut Butonları

Arayüzde bulunan hazır butonlar:
1. **For Döngüsü** - Örnek for döngüsü oluşturur
2. **String Değişken** - String değişken tanımlar
3. **Print Yaz** - Print komutu ekler
4. **Kodu Oku** - Mevcut kodu seslendirir

## 🛠️ Teknoloji Yığını

### Frontend
- **HTML5** - Yapısal tasarım
- **Tailwind CSS** - Modern styling
- **JavaScript (ES6+)** - Uygulama mantığı
- **CodeMirror 5** - Kod editörü

### AI & API'ler
- **Google Gemini 2.5 Flash** - Kod üretme
- **Gemini TTS** - Text-to-Speech
- **Web Speech API** - Ses tanıma

### Özellikler
- Modüler JavaScript mimarisi (IIFE pattern)
- Async/await kullanımı
- Error handling ve retry mekanizması
- WebSocket benzeri gerçek zamanlı feedback

## � Proje Yapısı

```
be_my_code/
├── index.html              # Ana uygulama dosyası
├── README.md              # Bu dosya
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Pages deployment
└── .gitignore             # Git ignore kuralları
```

### Kod Organizasyonu (index.html içinde)

```
App Module (IIFE)
├── CONFIG                 # Konfigürasyon sabitleri
├── State                  # Uygulama durumu
├── Elements               # DOM referansları
├── Utils                  # Yardımcı fonksiyonlar
│   ├── base64ToArrayBuffer
│   ├── pcmToWav
│   └── fetchWithRetry
├── UI                     # Kullanıcı arayüzü yönetimi
├── GeminiAPI              # AI API çağrıları
│   ├── generateCode
│   └── speak
├── CodeHandler            # Kod işleme
│   ├── speakCode
│   └── runSimulatedCode
├── VoiceRecognition       # Ses tanıma
│   ├── setup
│   └── toggle
└── Public API             # Global erişim
    ├── init
    ├── setupKeyboardShortcuts
    └── simulateCommand
```

## 🎨 Tasarım Renk Paleti

- **Ana Koyu (Dark BG):** `#1A181B`
- **Altın Sarısı (Accent):** `#D7BB56`
- **Açık Gri (Text):** `#EEECEE`
- **Koyu Gri (Secondary BG):** `#111827`

## 🔒 Güvenlik Notları

⚠️ **ÖNEMLİ:** API anahtarınızı asla public repository'lerde paylaşmayın!

**Öneriler:**
- Environment variables kullanın
- Backend API ile API anahtarını koruyun
- `.gitignore` dosyasına hassas bilgileri ekleyin
- GitHub Pages deployment'ta API key'i client-side'da tutmayın

## 🐛 Sorun Giderme

### Mikrofon Çalışmıyor
1. Tarayıcı ayarlarından mikrofon iznini kontrol edin
2. HTTPS veya localhost üzerinden çalıştığınızdan emin olun
3. F12 ile konsolu açın ve hata mesajlarını inceleyin

### Ses Çıkmıyor (TTS)
1. API anahtarının doğru olduğunu kontrol edin
2. İnternet bağlantınızı kontrol edin
3. Konsol loglarını inceleyin (`F12`)
4. İlk ses için sayfa ile etkileşim gerekebilir (butona tıklayın)

### Kod Üretilmiyor
1. Gemini API anahtarınızı kontrol edin
2. API kota limitinizi kontrol edin
3. Konsolda detaylı hata mesajlarını okuyun
4. İnternet bağlantınızı kontrol edin

## 📊 Proje İstatistikleri

- **Toplam Kod Satırı:** ~800 satır
- **JavaScript Modül Sayısı:** 7
- **Desteklenen Komut Türü:** Sınırsız (AI destekli)
- **Sürüm:** 2.0.0
- **Son Güncelleme:** Kasım 2025

## 🤝 Katkıda Bulunma

Bu proje TÜBİTAK 2209-A araştırma projesi kapsamında geliştirilmiştir. 

### Katkı Süreci
1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## � Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

Bu proje eğitim amaçlıdır ve açık kaynak olarak sunulmaktadır.

## � İletişim

**Proje Sahibi:** Erol Işıldak  
**E-posta:** [GitHub üzerinden iletişim]  
**Danışman:** Öğr. Gör. Gülsüm KEMERLİ  
**Proje Ortağı:** Harun Efe Akkan  
**Kurum:** Nuh Naci Yazgan Üniversitesi

## 🙏 Teşekkürler

- **TÜBİTAK 2209-A** programına destekleri için
- **Google** Gemini AI ekibine
- **Nuh Naci Yazgan Üniversitesi**'ne
- Tüm açık kaynak katkıcılarına

## 🌟 Proje Hedefleri

Bu proje ile:
- ♿ Teknolojiye erişimi demokratikleştirmek
- 📚 Görme engelli bireylerin kod öğrenmesini kolaylaştırmak
- 🤖 AI'ın eğitimde kullanımını göstermek
- 🎓 Üniversite öğrencilerine araştırma deneyimi sağlamak

---

<div align="center">

**"Teknoloji, herkes için erişilebilir olmalıdır"** 🌟

**Be My Code** - Ses ile kod yazmanın gücünü keşfedin!

TÜBİTAK 2209-A | Nuh Naci Yazgan Üniversitesi | 2025

[Demo](https://eisildak.github.io/be_my_code/) | [Dokümantasyon](#) | [Issues](https://github.com/eisildak/be_my_code/issues)

</div>
