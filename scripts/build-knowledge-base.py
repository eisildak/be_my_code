#!/usr/bin/env python3
"""
W3Schools Python Tutorial'ından bilgi çekerek 
Gemini destekli özel LLM bilgi tabanı oluşturur.

Kullanım:
    python3 build-knowledge-base.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from pathlib import Path

# W3Schools Python Tutorial URL'leri
PYTHON_URLS = [
    "https://www.w3schools.com/python/python_syntax.asp",
    "https://www.w3schools.com/python/python_output.asp",
    "https://www.w3schools.com/python/python_comments.asp",
    "https://www.w3schools.com/python/python_variables.asp",
    "https://www.w3schools.com/python/python_datatypes.asp",
    "https://www.w3schools.com/python/python_numbers.asp",
    "https://www.w3schools.com/python/python_casting.asp",
    "https://www.w3schools.com/python/python_strings.asp",
    "https://www.w3schools.com/python/python_booleans.asp",
    "https://www.w3schools.com/python/python_operators.asp",
    "https://www.w3schools.com/python/python_lists.asp",
    "https://www.w3schools.com/python/python_tuples.asp",
    "https://www.w3schools.com/python/python_sets.asp",
    "https://www.w3schools.com/python/python_dictionaries.asp",
    "https://www.w3schools.com/python/python_conditions.asp",
    "https://www.w3schools.com/python/python_match.asp",
    "https://www.w3schools.com/python/python_while_loops.asp",
    "https://www.w3schools.com/python/python_for_loops.asp",
    "https://www.w3schools.com/python/python_functions.asp",
    "https://www.w3schools.com/python/python_range.asp",
    "https://www.w3schools.com/python/python_arrays.asp",
    "https://www.w3schools.com/python/python_iterators.asp",
    "https://www.w3schools.com/python/python_modules.asp",
    "https://www.w3schools.com/python/python_datetime.asp",
    "https://www.w3schools.com/python/python_math.asp",
    "https://www.w3schools.com/python/python_json.asp",
    "https://www.w3schools.com/python/python_regex.asp",
    "https://www.w3schools.com/python/python_pip.asp",
    "https://www.w3schools.com/python/python_try_except.asp",
    "https://www.w3schools.com/python/python_string_formatting.asp",
    "https://www.w3schools.com/python/python_none.asp",
    "https://www.w3schools.com/python/python_user_input.asp",
    "https://www.w3schools.com/python/python_virtualenv.asp",
]

def scrape_w3schools_page(url):
    """W3Schools sayfasından içerik çeker"""
    try:
        print(f"📥 Çekiliyor: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Başlık
        title = soup.find('h1')
        title_text = title.get_text().strip() if title else "Başlık Yok"
        
        # Ana içerik
        main_content = soup.find('div', {'id': 'main'})
        
        if not main_content:
            print(f"⚠️ İçerik bulunamadı: {url}")
            return None
        
        # Kod örneklerini çek
        code_examples = []
        for code_block in main_content.find_all('div', class_='w3-code'):
            code_text = code_block.get_text().strip()
            if code_text:
                code_examples.append(code_text)
        
        # Açıklamaları çek (paragraflar)
        explanations = []
        for p in main_content.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 10:  # Çok kısa olanları filtrele
                explanations.append(text)
        
        # Önemli notları çek
        notes = []
        for note in main_content.find_all('div', class_=['w3-panel', 'note', 'intro']):
            note_text = note.get_text().strip()
            if note_text:
                notes.append(note_text)
        
        return {
            'url': url,
            'title': title_text,
            'code_examples': code_examples,
            'explanations': explanations[:5],  # İlk 5 açıklama
            'notes': notes,
            'topic': url.split('/')[-1].replace('.asp', '').replace('python_', '')
        }
    
    except Exception as e:
        print(f"❌ Hata ({url}): {e}")
        return None

def build_training_prompt(data):
    """Scrape edilen veriden training prompt oluşturur"""
    
    prompt_parts = []
    
    # Başlık
    prompt_parts.append(f"=== {data['title']} ===\n")
    prompt_parts.append(f"Konu: {data['topic']}\n")
    prompt_parts.append(f"Kaynak: {data['url']}\n\n")
    
    # Açıklamalar
    if data['explanations']:
        prompt_parts.append("📖 AÇIKLAMALAR:\n")
        for i, exp in enumerate(data['explanations'], 1):
            prompt_parts.append(f"{i}. {exp}\n")
        prompt_parts.append("\n")
    
    # Notlar
    if data['notes']:
        prompt_parts.append("⚠️ ÖNEMLİ NOTLAR:\n")
        for note in data['notes']:
            prompt_parts.append(f"- {note}\n")
        prompt_parts.append("\n")
    
    # Kod örnekleri
    if data['code_examples']:
        prompt_parts.append("💻 KOD ÖRNEKLERİ:\n")
        for i, code in enumerate(data['code_examples'], 1):
            prompt_parts.append(f"\nÖrnek {i}:\n```python\n{code}\n```\n")
    
    prompt_parts.append("\n" + "="*80 + "\n\n")
    
    return "".join(prompt_parts)

def main():
    """Ana fonksiyon"""
    print("🚀 W3Schools Python LLM Bilgi Tabanı Oluşturucu")
    print("=" * 80)
    
    # Çıktı klasörünü oluştur
    output_dir = Path(__file__).parent.parent / 'prompts' / 'knowledge'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_data = []
    full_training_text = []
    
    # Header
    header = """🎓 W3SCHOOLS PYTHON TUTORIAL - KAPSAMLI BİLGİ TABANI
Bu bilgi tabanı W3Schools Python Tutorial'ından otomatik olarak oluşturulmuştur.

📋 KULLANIM KURALLARI:
- Bu bilgiler görme engelli öğrenciler için Python kodu üretmek amacıyla kullanılır
- Sadece saf Python kodu döndürülmeli, açıklama yazılmamalı
- Python 3.8+ syntax kullanılmalı
- W3Schools best practices takip edilmeli

"""
    full_training_text.append(header)
    
    # Her URL'i scrape et
    for i, url in enumerate(PYTHON_URLS, 1):
        print(f"\n[{i}/{len(PYTHON_URLS)}] İşleniyor...")
        
        data = scrape_w3schools_page(url)
        if data:
            all_data.append(data)
            training_prompt = build_training_prompt(data)
            full_training_text.append(training_prompt)
            
            # Bireysel dosya kaydet
            topic_file = output_dir / f"{data['topic']}.txt"
            with open(topic_file, 'w', encoding='utf-8') as f:
                f.write(training_prompt)
            print(f"✅ Kaydedildi: {topic_file.name}")
        
        # Rate limiting
        time.sleep(1)
    
    # Tüm bilgiyi tek dosyada birleştir
    combined_file = output_dir.parent / 'python-knowledge-complete.txt'
    with open(combined_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(full_training_text))
    
    print(f"\n✅ Birleştirilmiş dosya: {combined_file}")
    
    # JSON olarak da kaydet (API için)
    json_file = output_dir.parent / 'python-knowledge.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON formatı: {json_file}")
    
    # İstatistikler
    print("\n" + "=" * 80)
    print("📊 İSTATİSTİKLER:")
    print(f"   📄 Toplam sayfa: {len(all_data)}")
    print(f"   💻 Toplam kod örneği: {sum(len(d['code_examples']) for d in all_data)}")
    print(f"   📝 Toplam açıklama: {sum(len(d['explanations']) for d in all_data)}")
    print(f"   📦 Toplam boyut: {len(''.join(full_training_text))} karakter")
    print(f"   📂 Klasör: {output_dir}")
    print("=" * 80)
    
    print("\n🎉 Bilgi tabanı başarıyla oluşturuldu!")
    print(f"\n💡 Kullanım: index.html dosyasında PROMPT_FILE = '{combined_file.relative_to(Path(__file__).parent.parent)}'")

if __name__ == "__main__":
    main()
