# Be My Code - Hızlı Başlangıç Kılavuzu

## Kurulum

### 1. Gereksinimleri Yükle

```bash
# Kurulum scriptini çalıştırılabilir yap
chmod +x install.sh

# Kurulumu başlat
./install.sh
```

### 2. Sanal Ortamı Aktif Et

```bash
source venv/bin/activate
```

### 3. Uygulamayı Başlat

```bash
python src/main.py
```

## Temel Kullanım

### Ses Komutları

1. **Mikrofon simgesine tıklayın** veya `Ctrl+M` tuşuna basın
2. Komutunuzu söyleyin
3. Kod otomatik olarak editöre eklenecektir

### Desteklenen Komutlar

#### Değişken Tanımlama
- "string değişken"
- "integer değişken adı sayı"
- "float değişken"
- "boolean değişken"
- "liste değişken"

#### Döngüler
- "for döngüsü yaz"
- "while döngüsü oluştur"

#### Koşullar
- "if koşulu"

#### Fonksiyonlar
- "fonksiyon tanımla"
- "fonksiyon tanımla hesapla"

#### Diğer
- "yazdır" (print)
- "girdi al" (input)
- "yorum bu bir test yorumu"

### Klavye Kısayolları

| Kısayol | Fonksiyon |
|---------|-----------|
| `Ctrl+M` | Ses komutu al |
| `Ctrl+R` | Tüm kodu oku |
| `Ctrl+L` | Geçerli satırı oku |
| `F5` | Kodu çalıştır |
| `Ctrl+Space` | Kod önerisi al |
| `Ctrl+N` | Yeni dosya |
| `Ctrl+O` | Dosya aç |
| `Ctrl+S` | Dosyayı kaydet |

## Özellikler

### 1. Dosya Yöneticisi
- Sol panelde dosyalarınızı görüntüleyin
- Dosyalara çift tıklayarak açın
- Yeni dosya oluşturun

### 2. Kod Editörü
- Syntax highlighting
- Büyük font boyutu (görme zorluğu için)
- Koyu tema (göz yorgunluğunu azaltır)

### 3. Ses Sistemi
- **Dinleme**: Türkçe ses komutları
- **Okuma**: Coqui-XTTS v2 ile profesyonel Türkçe seslendirme
- **Kod Okuma**: Yazılan kodları Türkçe olarak okur

### 4. Terminal
- Kod çıktılarını görüntüleme
- Hata mesajlarını sesli duyma

## Örnek Çalışma Akışı

1. **Yeni Dosya Oluştur**
   - "Dosya" > "Yeni" veya `Ctrl+N`

2. **Ses ile Kod Yaz**
   - `Ctrl+M` tuşuna basın
   - "for döngüsü yaz" deyin
   - Kod otomatik oluşur

3. **Kodu Dinle**
   - `Ctrl+R` ile tüm kodu dinleyin
   - `Ctrl+L` ile sadece bir satırı dinleyin

4. **Çalıştır**
   - `F5` tuşuna basın
   - Terminalde çıktıyı görün

5. **Kaydet**
   - `Ctrl+S` ile kaydedin

## Sorun Giderme

### Mikrofon Çalışmıyor
```bash
# Mikrofon izinlerini kontrol edin
# macOS: Sistem Ayarları > Gizlilik > Mikrofon
```

### TTS Modeli Yüklenmiyor
```bash
# Manuel model indirme
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### PyAudio Hatası
```bash
# macOS için portaudio yükleyin
brew install portaudio

# Sonra PyAudio'yu tekrar yükleyin
pip install pyaudio
```

## Gelişmiş Ayarlar

### .env Dosyası

```env
# TTS Ayarları
TTS_LANGUAGE=tr
TTS_MODEL=tts_models/multilingual/multi-dataset/xtts_v2

# Ses Tanıma
SPEECH_RECOGNITION_LANGUAGE=tr-TR
SPEECH_RECOGNITION_ENERGY_THRESHOLD=4000

# Debug
DEBUG_MODE=True
LOG_LEVEL=INFO
```

### Referans Ses Dosyası
Daha doğal seslendirme için:
1. 6-10 saniyelik Türkçe konuşma örneği kaydedin (WAV formatı)
2. `assets/reference_audio/speaker.wav` olarak kaydedin
3. `.env` dosyasında yolu belirtin

## Katkıda Bulunma

Bu proje TÜBİTAK 2209-A kapsamında eğitim amaçlıdır.

## İletişim

**Proje Sahibi**: Erol Işıldak  
**Danışman**: Öğr. Gör. Gülsüm KEMERLİ  
**Kurum**: Nuh Naci Yazgan Üniversitesi
