#!/bin/bash

# Be My Code IDE Başlatıcı Script

echo "================================================"
echo "Be My Code IDE Başlatılıyor..."
echo "================================================"

# Proje dizinine git
cd "$(dirname "$0")"

# Sanal ortam aktif mi kontrol et
if [ -z "$VIRTUAL_ENV" ]; then
    echo "\nSanal ortam aktif ediliyor..."
    source venv/bin/activate
fi

# Python ve paketleri kontrol et
if ! python -c "import PyQt5" 2>/dev/null; then
    echo "\n⚠️  Gerekli paketler yüklü değil!"
    echo "Lütfen önce kurulum yapın: ./install.sh"
    exit 1
fi

# Uygulamayı başlat
echo "\n✅ Tüm kontroller başarılı!"
echo "IDE başlatılıyor...\n"

python src/main.py

echo "\n================================================"
echo "IDE kapatıldı."
echo "================================================"
