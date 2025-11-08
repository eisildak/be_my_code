"""
Be My Code - Görme Engelli Bireyler için Kod Yazma Asistan Programı
Ana giriş noktası

Proje Sahibi: Erol Işıldak
Danışman: Öğr. Gör. Gülsüm KEMERLİ
Proje Ortağı: Harun Efe Akkan
"""

import sys
import os
from pathlib import Path

# Proje kök dizinini Python path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

from modules.logger import setup_logger
from ui.main_window import MainWindow

# Environment değişkenlerini yükle
load_dotenv()

# Logger'ı ayarla
logger = setup_logger()


def main():
    """Ana uygulama başlatıcı"""
    logger.info("=" * 60)
    logger.info("Be My Code IDE Başlatılıyor...")
    logger.info("=" * 60)
    
    # Yüksek DPI desteği
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Be My Code")
    app.setOrganizationName("TÜBİTAK 2209-A")
    
    # Ana pencereyi oluştur
    window = MainWindow()
    window.show()
    
    logger.info("Uygulama başarıyla başlatıldı!")
    logger.info("Ses komutları için mikrofon simgesine tıklayın veya Ctrl+M kullanın")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
