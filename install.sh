#!/bin/bash

# Be My Code IDE Kurulum Scripti
# macOS için

echo "================================================"
echo "Be My Code IDE Kurulum Başlatılıyor..."
echo "================================================"

# Python sürümünü kontrol et
echo "\n1. Python sürümü kontrol ediliyor..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 bulunamadı! Lütfen Python 3.8+ yükleyin."
    exit 1
fi

# Sanal ortam oluştur
echo "\n2. Sanal ortam oluşturuluyor..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Sanal ortam oluşturulamadı!"
    exit 1
fi

# Sanal ortamı aktif et
echo "\n3. Sanal ortam aktif ediliyor..."
source venv/bin/activate

# Pip'i güncelle
echo "\n4. pip güncelleniyor..."
pip install --upgrade pip

# PyAudio için gerekli sistem bağımlılıkları (macOS)
echo "\n5. Sistem bağımlılıkları kontrol ediliyor..."
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew bulunamadı. PyAudio için portaudio gerekli."
    echo "Homebrew kurulumu için: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
else
    echo "Installing portaudio for PyAudio..."
    brew install portaudio
fi

# Bağımlılıkları yükle
echo "\n6. Python paketleri yükleniyor..."
echo "Bu işlem birkaç dakika sürebilir..."

pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Paket yüklemesi başarısız!"
    echo "Manuel kurulum: pip install -r requirements.txt"
    exit 1
fi

# .env dosyası oluştur
echo "\n7. Yapılandırma dosyası oluşturuluyor..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env dosyası oluşturuldu. API anahtarlarınızı ekleyebilirsiniz."
else
    echo "⚠️  .env dosyası zaten mevcut."
fi

# Workspace dizini oluştur
echo "\n8. Workspace dizini oluşturuluyor..."
mkdir -p ~/BeMyCode_Workspace
mkdir -p logs
mkdir -p assets/reference_audio

echo "\n================================================"
echo "✅ Kurulum tamamlandı!"
echo "================================================"
echo ""
echo "Uygulamayı başlatmak için:"
echo "  source venv/bin/activate"
echo "  python src/main.py"
echo ""
echo "Not: İlk çalıştırmada Coqui-XTTS v2 modeli indirilecektir."
echo "Bu işlem internet bağlantınıza bağlı olarak zaman alabilir."
echo ""
