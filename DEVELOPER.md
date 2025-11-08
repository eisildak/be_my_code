# Geliştirici Notları

## 🚀 Kurulum ve Başlatma

### İlk Kurulum
```bash
# 1. Depoyu klonla veya indir
git clone <repo-url> be_my_code
cd be_my_code

# 2. Kurulum scriptini çalıştır
./install.sh

# 3. Sanal ortamı aktif et
source venv/bin/activate

# 4. .env dosyasını düzenle (opsiyonel API anahtarları)
cp .env.example .env
nano .env

# 5. Uygulamayı başlat
./run.sh
# veya
python src/main.py
```

### Gereksinimler
- Python 3.8+
- macOS (Linux/Windows için install.sh değişikliği gerekir)
- Mikrofon erişimi
- ~3GB disk alanı (TTS modeli için)
- İnternet bağlantısı (ilk çalıştırma ve STT için)

## 🔧 Geliştirme

### Yeni Modül Ekleme
1. `src/modules/` altında yeni dosya oluştur
2. Logger'ı import et: `from modules.logger import setup_logger`
3. `__init__.py` dosyasına ekle
4. Ana kodda import et

### Yeni Ses Komutu Ekleme
1. `src/modules/nlp_processor.py` dosyasını aç
2. `_initialize_patterns()` fonksiyonuna yeni pattern ekle
3. İşleyici fonksiyon oluştur (örn: `_create_new_command`)
4. Test et

Örnek:
```python
# Pattern ekle
r'sözlük\s+(değişken|degisken)?\s*(\w+)?': self._create_dict_variable,

# İşleyici fonksiyon
def _create_dict_variable(self, match, command: str) -> str:
    var_name = self._extract_variable_name(match, command, default="sozluk")
    return f'{var_name} = {{}}'
```

### UI Özelleştirme
- Renkler: `src/ui/main_window.py` içinde stylesheet'ler
- Font boyutu: `src/config.py` → `EDITOR_FONT_SIZE`
- Pencere boyutu: `src/config.py` → `WINDOW_WIDTH`, `WINDOW_HEIGHT`

## 🎯 Önemli Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `src/main.py` | Uygulama giriş noktası |
| `src/ui/main_window.py` | Ana pencere ve tüm UI logic |
| `src/modules/nlp_processor.py` | Komut işleme beyni |
| `src/modules/text_to_speech.py` | TTS sistemi |
| `src/modules/speech_recognizer.py` | STT sistemi |
| `src/config.py` | Tüm ayarlar |

## 🐛 Debug

### Log Dosyaları
```bash
# En son log dosyasını görüntüle
tail -f logs/be_my_code_*.log
```

### Debug Modu
`.env` dosyasında:
```env
DEBUG_MODE=True
LOG_LEVEL=DEBUG
```

### Mikrofon Testi
```bash
python -c "from src.modules.speech_recognizer import SpeechRecognizer; rec = SpeechRecognizer(); rec.test_microphone()"
```

### TTS Testi
```bash
python -c "from src.modules.text_to_speech import TextToSpeech; tts = TextToSpeech(); tts.speak('Test mesajı')"
```

## 📦 Bağımlılık Yönetimi

### Yeni Paket Ekleme
```bash
# Paketi yükle
pip install yeni-paket

# requirements.txt'i güncelle
pip freeze > requirements.txt
```

### Güncelleme
```bash
pip install --upgrade -r requirements.txt
```

## 🔊 TTS Özelleştirme

### Referans Ses Kaydetme
1. Ses kaydedici ile 6-10 saniyelik temiz Türkçe konuşma kaydet
2. WAV formatında kaydet (16kHz önerilir)
3. `assets/reference_audio/speaker.wav` olarak kaydet
4. `.env` dosyasında yolu belirt:
   ```env
   TTS_SPEAKER_WAV=assets/reference_audio/speaker.wav
   ```

### TTS Modelini Değiştirme
```env
# Başka bir XTTS modeli kullan
TTS_MODEL=tts_models/multilingual/multi-dataset/xtts_v2
```

## 🎤 STT Özelleştirme

### Gürültü Eşiği Ayarlama
```env
# Daha hassas (sessiz ortam)
SPEECH_RECOGNITION_ENERGY_THRESHOLD=3000

# Daha az hassas (gürültülü ortam)
SPEECH_RECOGNITION_ENERGY_THRESHOLD=5000
```

### Offline STT (Gelecek)
Şu an Google API kullanılıyor (internet gerekli).
Offline için: Vosk, Whisper gibi modeller eklenebilir.

## 🧪 Test

### Unit Testler
```bash
# NLP testleri
python src/modules/nlp_processor.py

# Code analyzer testleri
python src/modules/code_analyzer.py

# Utils testleri
python src/modules/utils.py
```

### Manuel Test Checklist
- [ ] Mikrofon algılanıyor
- [ ] Ses komutları çalışıyor
- [ ] TTS seslendirme yapılıyor
- [ ] Dosya açma/kaydetme
- [ ] Kod çalıştırma
- [ ] Terminal çıktı
- [ ] Klavye kısayolları

## 📊 Performans İzleme

### Ses Tanıma Süresi
```python
import time
start = time.time()
text = recognizer.listen_once()
print(f"Süre: {time.time() - start:.2f} sn")
```

### TTS Üretim Süresi
```python
import time
start = time.time()
tts.speak("Test")
print(f"Süre: {time.time() - start:.2f} sn")
```

## 🔐 Güvenlik Notları

### Kod Çalıştırma
**ÖNEMLİ**: Şu an `exec()` ile kod çalıştırılıyor - GÜVENSİZ!

Gelecek sürümler için:
- Sandbox ortamı (RestrictedPython)
- Docker container
- Timeout mekanizması
- Dosya sistemi kısıtlamaları

### API Anahtarları
`.env` dosyası `.gitignore`'da - asla commit etmeyin!

## 🌍 Çoklu Dil Desteği

### İngilizce TTS Ekleme
```python
# text_to_speech.py içinde
if language == "en":
    self.tts.tts_to_file(text=text, file_path=save_path, language="en")
```

### İngilizce STT
```python
# speech_recognizer.py içinde
self.language = "en-US"
```

## 📝 Kod Stilleri

### Python Style Guide
- PEP 8 kuralları
- Fonksiyon docstring'leri
- Type hints (opsiyonel)
- Max line length: 100

### Örnek Docstring
```python
def fonksiyon(param1: str, param2: int) -> bool:
    """
    Fonksiyon açıklaması
    
    Args:
        param1: İlk parametre
        param2: İkinci parametre
    
    Returns:
        bool: Sonuç
    """
    pass
```

## 🚨 Bilinen Sorunlar

1. **PyAudio Kurulumu**: macOS'ta portaudio gerekiyor
   ```bash
   brew install portaudio
   ```

2. **TTS İlk İndirme**: ~2GB model indiriliyor, uzun sürebilir

3. **Mikrofon İzinleri**: macOS Sistem Ayarları'ndan izin gerekli

4. **Google STT Limitler**: Günlük API limiti var (ücretsiz tier)

## 💡 İpuçları

- İlk çalıştırmada TTS modeli indiriliyor, sabırlı ol
- Mikrofonu çalıştırmadan önce test et
- Log dosyalarını düzenli kontrol et
- Ses kalitesi için iyi mikrofon kullan
- Gürültülü ortamda SPEECH_ENERGY_THRESHOLD'u artır

## 📞 Destek

Sorunlar için:
1. Log dosyalarını kontrol et
2. `TESTING.md` dosyasındaki test senaryolarını çalıştır
3. GitHub issues (varsa)
4. Danışman: Öğr. Gör. Gülsüm KEMERLİ

## 🎓 Öğrenme Kaynakları

- [PyQt5 Tutorial](https://www.pythonguis.com/pyqt5-tutorial/)
- [Coqui TTS Docs](https://tts.readthedocs.io/)
- [SpeechRecognition Guide](https://realpython.com/python-speech-recognition/)
- [Python Best Practices](https://realpython.com/tutorials/best-practices/)

---

**Son Güncelleme**: 2025-11-08  
**Geliştirici**: Erol Işıldak  
**Proje**: TÜBİTAK 2209-A
