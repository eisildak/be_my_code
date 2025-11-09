# 🤖 W3Schools Python LLM Bilgi Tabanı

Bu araç W3Schools Python Tutorial sayfalarından otomatik olarak bilgi çekerek, Gemini AI destekli özel bir Python LLM bilgi tabanı oluşturur.

## 📊 Oluşturulan Bilgi Tabanı

- **33 Python Konusu** (syntax, variables, loops, functions, OOP, vb.)
- **257 Gerçek Kod Örneği** W3Schools'dan
- **161 Detaylı Açıklama** ve best practices
- **52,656 Karakter** kapsamlı eğitim verisi
- **2,498 Satır** toplam içerik

## 🚀 Kullanım

### 1. Gerekli Paketleri Kurma

```bash
cd scripts
pip3 install -r requirements.txt
```

veya Python virtual environment ile:

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
pip install -r scripts/requirements.txt
```

### 2. Scraper'ı Çalıştırma

```bash
python3 scripts/build-knowledge-base.py
```

### 3. Çıktılar

Script çalıştırıldığında şu dosyalar oluşur:

```
prompts/
├── python-knowledge-complete.txt  # Tüm bilgiler birleştirilmiş (index.html'de kullanılıyor)
├── python-knowledge.json          # JSON formatında API için
└── knowledge/                     # Her konu ayrı dosyada
    ├── syntax.txt
    ├── variables.txt
    ├── loops.txt
    ├── functions.txt
    └── ... (33 dosya)
```

## 📚 Scrape Edilen Konular

1. **Python Basics**: Syntax, Output, Comments, Variables, Data Types
2. **Veri Yapıları**: Numbers, Strings, Booleans, Lists, Tuples, Sets, Dictionaries
3. **Kontrol Akışı**: If-Else, Match, While Loops, For Loops
4. **Fonksiyonlar**: Functions, Lambda, Range, Iterators
5. **İleri Seviye**: Classes, Modules, Exceptions, File Handling
6. **Kütüphaneler**: DateTime, Math, JSON, RegEx, PIP
7. **Diğer**: Type Casting, String Formatting, User Input, Virtual Environment

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

- **Python 3.8+**
- **requests**: HTTP istekleri için
- **BeautifulSoup4**: HTML parsing
- **lxml**: HTML/XML işleme

### Scraper Özellikleri

✅ Her sayfadan otomatik olarak çeker:
- Başlıklar ve konular
- Kod örnekleri (`<div class="w3-code">`)
- Açıklamalar (paragraflar)
- Önemli notlar ve uyarılar
- URL ve metadata

✅ Rate limiting (sayfa başına 1 saniye bekleme)
✅ Hata toleranslı (bir sayfa hata verse bile devam eder)
✅ İlerlemeli log çıktısı

## 📖 Örnek Kullanım

### Manuel Kullanım

```python
# Tek bir sayfayı scrape et
from build_knowledge_base import scrape_w3schools_page

data = scrape_w3schools_page("https://www.w3schools.com/python/python_syntax.asp")
print(data['code_examples'])
```

### Bilgi Tabanını Güncelleme

Yeni W3Schools sayfaları eklemek için:

1. `build-knowledge-base.py` dosyasını açın
2. `PYTHON_URLS` listesine yeni URL'leri ekleyin
3. Script'i tekrar çalıştırın

```python
PYTHON_URLS = [
    # ... mevcut URL'ler ...
    "https://www.w3schools.com/python/yeni_konu.asp",  # YENİ
]
```

## 🎯 LLM Entegrasyonu

Oluşturulan `python-knowledge-complete.txt` dosyası direkt olarak `index.html`'de kullanılır:

```javascript
// index.html içinde
const CONFIG = {
    PROMPT_FILE: 'prompts/python-knowledge-complete.txt'
};

async function loadSystemPrompt() {
    const response = await fetch(CONFIG.PROMPT_FILE);
    CONFIG.SYSTEM_PROMPT = await response.text();
}
```

## 📈 Performans

- **Scraping Süresi**: ~35 saniye (33 sayfa)
- **Toplam Boyut**: ~52 KB metin
- **Gemini API Token Kullanımı**: Optimize edilmiş

## 🔄 Güncelleme Sıklığı

W3Schools güncellemelerini takip etmek için:
- Script'i periyodik olarak çalıştırın (örn: ayda 1 kez)
- Git diff ile değişiklikleri kontrol edin
- Önemli güncellemeleri commit edin

## 🛠️ Özelleştirme

### Farklı Kaynaklar Eklemek

```python
# Yeni bir kaynak eklemek için scrape fonksiyonunu genişletin
def scrape_custom_site(url):
    # Özel parsing mantığınız
    pass
```

### Bilgi Tabanı Formatı

Output formatını değiştirmek için `build_training_prompt()` fonksiyonunu düzenleyin.

## 📝 Lisans

Bu araç eğitim amaçlıdır. W3Schools içeriği [W3Schools Terms of Use](https://www.w3schools.com/about/about_copyright.asp)'a tabidir.

## 🤝 Katkıda Bulunma

1. Yeni W3Schools sayfaları ekleyin
2. Scraping mantığını iyileştirin
3. Hata düzeltmeleri yapın
4. Dokümantasyonu geliştirin

## 📞 İletişim

Sorular veya öneriler için GitHub Issues kullanın.

---

**Not**: Bu araç TÜBİTAK 2209-A "Be My Code" projesi kapsamında geliştirilmiştir.
