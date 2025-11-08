# 🎤 Be My Code

Görme engelli bireyler için tasarlanmış, sesli komutlarla Python kod yazan AI destekli bir eğitim platformu.

## ✨ Özellikler

- 🎙️ **Sesli Komut Desteği**: Türkçe ses tanıma ile kod yazın
- 🤖 **Gemini AI Entegrasyonu**: Doğal dille Python kodu üretin
- 🔊 **Sesli Geri Bildirim**: Text-to-Speech ile kodunuzu dinleyin
- ⌨️ **Klavye Kısayolları**: Hızlı erişim için kısayollar
- 🎨 **Erişilebilir Tasarım**: Yüksek kontrast ve büyük fontlar

## 🚀 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/eisildak/be_my_code.git
cd be_my_code
```

### 2. Gemini API Anahtarı Alın

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın
3. API anahtarınızı kopyalayın

### 3. API Anahtarını Yapılandırın

`index.html` dosyasını açın ve şu satırı bulun (yaklaşık 263. satır):

```javascript
const CONFIG = {
    GEMINI_API_KEY: "",  // ← Buraya API anahtarınızı yapıştırın
    // ...
};
```

API anahtarınızı tırnak işaretleri arasına yapıştırın:

```javascript
const CONFIG = {
    GEMINI_API_KEY: "YOUR_API_KEY_HERE",
    // ...
};
```

### 4. Uygulamayı Çalıştırın

```bash
# Python 3 ile basit HTTP sunucu
python3 -m http.server 8000

# veya Node.js varsa
npx http-server -p 8000
```

Tarayıcınızda `http://localhost:8000` adresini açın.

## 🎯 Kullanım

### Klavye Kısayolları

- **Ctrl+M** / **Cmd+M**: Mikrofonu aç/kapat
- **F5**: Kodu çalıştır (simülasyon)
- **Ctrl+R** / **Cmd+R**: Kodu sesli oku

### Sesli Komut Örnekleri

- `"for döngüsü yaz"`
- `"print fonksiyonu yaz Merhaba Dünya"`
- `"string değişken tanımla isim"`
- `"if else koşulu yaz"`
- `"kodu sesli oku"`
- `"kodu çalıştır"`

### Hızlı Komut Butonları

Arayüzde bulunan hızlı komut butonlarına tıklayarak örnek komutları deneyebilirsiniz.

## 🛠️ Teknolojiler

- **Frontend**: HTML5, Tailwind CSS, CodeMirror
- **AI**: Google Gemini API (Text & TTS)
- **Ses Tanıma**: Web Speech API (Chrome/Edge)
- **Database**: Firebase (isteğe bağlı)

## 📋 Sistem Gereksinimleri

- Modern web tarayıcısı (Chrome, Edge önerilir)
- Mikrofon erişimi
- İnternet bağlantısı (API çağrıları için)

## 🔒 Güvenlik Notu

⚠️ **ÖNEMLİ**: API anahtarınızı asla public repository'lere commit etmeyin!

Üretim ortamı için:
- Environment variables kullanın
- Backend API ile API anahtarını saklayın
- `.gitignore` dosyasına API anahtarlarını ekleyin

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**eisildak**
- GitHub: [@eisildak](https://github.com/eisildak)

## 🙏 Teşekkürler

- Google Gemini AI ekibine
- Açık kaynak toplulığuna
- Tüm katkıda bulunanlara

## 📞 İletişim

Sorularınız veya önerileriniz için GitHub Issues kullanabilirsiniz.

---

**Not**: Bu uygulama eğitim amaçlıdır. Üretim ortamında kullanmadan önce güvenlik ve performans testleri yapılmalıdır.
