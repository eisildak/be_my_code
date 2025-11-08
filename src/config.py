"""
Yapılandırma dosyası - Uygulama ayarları
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


class Config:
    """Uygulama yapılandırması"""
    
    # Proje yolları
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = BASE_DIR / "src"
    ASSETS_DIR = BASE_DIR / "assets"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Workspace
    WORKSPACE_DIR = Path.home() / "BeMyCode_Workspace"
    
    # TTS Ayarları
    TTS_MODEL = os.getenv("TTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")
    TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "tr")
    TTS_SPEAKER_WAV = os.getenv("TTS_SPEAKER_WAV", None)
    
    # Speech Recognition Ayarları
    SPEECH_LANGUAGE = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "tr-TR")
    SPEECH_ENERGY_THRESHOLD = int(os.getenv("SPEECH_RECOGNITION_ENERGY_THRESHOLD", "4000"))
    
    # API Keys (Opsiyonel)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", None)
    
    # Debug
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # UI Ayarları
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    EDITOR_FONT_SIZE = 14
    EDITOR_FONT_FAMILY = "Consolas"
    
    # Kod Editörü Ayarları
    TAB_SIZE = 4
    AUTO_INDENT = True
    SHOW_LINE_NUMBERS = True
    
    # Ses Komutları
    VOICE_COMMAND_TIMEOUT = 5  # saniye
    VOICE_PHRASE_LIMIT = 10  # saniye
    
    @classmethod
    def ensure_directories(cls):
        """Gerekli dizinleri oluştur"""
        cls.WORKSPACE_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.ASSETS_DIR.mkdir(exist_ok=True)
        (cls.ASSETS_DIR / "reference_audio").mkdir(exist_ok=True)


# Başlangıçta dizinleri oluştur
Config.ensure_directories()
