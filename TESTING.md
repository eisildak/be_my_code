# Be My Code Test Suite

## Test Senaryoları

### 1. Mikrofon Testi
```bash
python -c "
from src.modules.speech_recognizer import SpeechRecognizer
rec = SpeechRecognizer()
print('Mikrofon testi:', 'BAŞARILI' if rec.test_microphone() else 'BAŞARISIZ')
"
```

### 2. TTS Testi
```bash
python -c "
from src.modules.text_to_speech import TextToSpeech
tts = TextToSpeech()
tts.speak('Merhaba, test mesajı.')
print('TTS testi tamamlandı')
"
```

### 3. NLP Testi
```bash
python -c "
from src.modules.nlp_processor import NLPProcessor
nlp = NLPProcessor()
test_commands = ['for döngüsü yaz', 'string değişken', 'while döngüsü']
for cmd in test_commands:
    code = nlp.process_command(cmd)
    print(f'Komut: {cmd}')
    print(f'Kod: {code}\n')
"
```

### 4. Tam Uygulama Testi
```bash
python src/main.py
```

## Test Checklist

- [ ] Mikrofon algılanıyor
- [ ] Ses tanıma çalışıyor (Türkçe)
- [ ] TTS modeli yükleniyor
- [ ] Türkçe seslendirme yapılıyor
- [ ] NLP komutları işleniyor
- [ ] Kod editörü açılıyor
- [ ] Dosya yöneticisi çalışıyor
- [ ] Klavye kısayolları aktif
- [ ] Kod çalıştırma fonksiyonu çalışıyor
- [ ] Dosya kaydetme/açma çalışıyor

## Performans Testleri

### Ses Tanıma Hızı
- Beklenen: < 2 saniye

### TTS Üretim Hızı
- Kısa cümle (10 kelime): < 3 saniye
- Uzun metin (50 kelime): < 10 saniye

### NLP İşleme
- Komut tanıma: < 0.5 saniye

## Kullanıcı Testleri (Harun Efe Akkan ile)

### Erişilebilirlik
1. Klavye navigasyonu
2. Ses komutları netliği
3. TTS okunabilirliği
4. Hata mesajları anlaşılabilirliği

### Kullanılabilirlik
1. Kod yazma kolaylığı
2. Dosya yönetimi
3. Hata düzeltme
4. Öğrenme eğrisi

### Verimlilik
1. Kod yazma hızı (öncesi/sonrası)
2. Hata oranı
3. Görev tamamlama süresi

## Hata Senaryoları

### Mikrofon Hatası
- Kullanıcıya net mesaj gösterilmeli
- Alternatif input yöntemi önerilmeli

### İnternet Bağlantısı Sorunu
- Çevrimdışı mod devreye girmeli
- TTS cache kullanılmalı

### Tanınmayan Komut
- Kullanıcıya geri bildirim verilmeli
- Alternatif komutlar önerilmeli

## Güvenlik Testleri

### Kod Çalıştırma
- [ ] Sandbox ortamı (gelecek sürüm)
- [ ] Zararlı kod koruması
- [ ] Dosya sistemi izinleri

## Notlar
- Her test sonrası logs/ dizinini kontrol edin
- Kullanıcı geri bildirimleri kaydedin
- Performans metriklerini ölçün
