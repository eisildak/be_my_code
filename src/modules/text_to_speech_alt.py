"""
Text-to-Speech modülü - Alternatif TTS motorları
pyttsx3 (offline) veya gTTS (Google) ile çalışır
"""

import os
from typing import Optional
import tempfile
from pathlib import Path

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

try:
    import pygame
    import pygame.mixer
    HAS_PYGAME = True
except (ImportError, NotImplementedError):
    HAS_PYGAME = False

from modules.logger import setup_logger

logger = setup_logger()


class TextToSpeech:
    """Text-to-Speech sınıfı - pyttsx3 veya gTTS kullanır"""
    
    def __init__(self):
        self.language = os.getenv("TTS_LANGUAGE", "tr")
        self.engine_type = "pyttsx3" if HAS_PYTTSX3 else "gtts"
        
        logger.info(f"TTS modülü başlatılıyor... (Motor: {self.engine_type})")
        
        if HAS_PYTTSX3:
            self._init_pyttsx3()
        elif HAS_GTTS:
            logger.info("Google TTS (gTTS) kullanılıyor - internet bağlantısı gerekli")
        else:
            logger.error("Hiçbir TTS motoru bulunamadı! pyttsx3 veya gTTS yükleyin.")
        
        # Pygame mixer (opsiyonel - sadece gTTS için gerekli)
        if HAS_PYGAME:
            try:
                pygame.mixer.init()
                logger.info("Pygame mixer başlatıldı (gTTS ses oynatma için)")
            except Exception as e:
                logger.warning(f"Pygame mixer başlatılamadı: {e}")
    
    def _init_pyttsx3(self):
        """pyttsx3 motorunu başlat"""
        try:
            self.engine = pyttsx3.init()
            
            # Türkçe ses seç (macOS'ta türkçe ses varsa)
            voices = self.engine.getProperty('voices')
            
            # Türkçe veya kadın ses ara
            for voice in voices:
                if 'turkish' in voice.name.lower() or 'tr' in voice.languages[0].lower():
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Türkçe ses bulundu: {voice.name}")
                    break
            
            # Hız ve ses seviyesi ayarla
            self.engine.setProperty('rate', 150)  # Konuşma hızı
            self.engine.setProperty('volume', 0.9)  # Ses seviyesi
            
            logger.info("pyttsx3 TTS motoru başarıyla başlatıldı")
        except Exception as e:
            logger.error(f"pyttsx3 başlatma hatası: {e}")
            self.engine = None
    
    def speak(self, text: str, save_path: Optional[str] = None, play: bool = True) -> Optional[str]:
        """
        Metni seslendir
        
        Args:
            text: Seslendirilecek metin
            save_path: Ses dosyasını kaydetme yolu
            play: Ses dosyasını otomatik oynat
        
        Returns:
            str: Oluşturulan ses dosyası yolu veya None
        """
        if not text or text.strip() == "":
            logger.warning("Boş metin seslendirilemez")
            return None
        
        logger.info(f"Seslendiriliyor: {text[:50]}...")
        
        try:
            if self.engine_type == "pyttsx3" and HAS_PYTTSX3 and self.engine:
                return self._speak_pyttsx3(text, save_path, play)
            elif HAS_GTTS:
                return self._speak_gtts(text, save_path, play)
            else:
                logger.error("TTS motoru mevcut değil!")
                print(f"TTS: {text}")  # Fallback: konsola yazdır
                return None
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
            return None
    
    def _speak_pyttsx3(self, text: str, save_path: Optional[str], play: bool) -> Optional[str]:
        """pyttsx3 ile seslendir"""
        if save_path:
            self.engine.save_to_file(text, save_path)
            self.engine.runAndWait()
            logger.info(f"Ses dosyası kaydedildi: {save_path}")
            
            if play and HAS_PYGAME:
                self.play_audio(save_path)
            
            return save_path
        else:
            # macOS'ta direkt 'say' komutunu kullan (daha güvenilir)
            import subprocess
            import platform
            
            if platform.system() == 'Darwin':  # macOS
                try:
                    # Türkçe ses ile say komutu
                    subprocess.run(['say', '-v', 'Yelda', text], check=False)
                    logger.info(f"macOS 'say' komutuyla seslendirme başarılı")
                    return None
                except Exception as e:
                    logger.warning(f"'say' komutu hatası: {e}, pyttsx3'e geçiliyor")
            
            # Fallback: pyttsx3 kullan
            self.engine.say(text)
            self.engine.runAndWait()
            return None
    
    def _speak_gtts(self, text: str, save_path: Optional[str], play: bool) -> Optional[str]:
        """gTTS ile seslendir"""
        if save_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            save_path = temp_file.name
            temp_file.close()
        
        # gTTS ile ses oluştur
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save(save_path)
        logger.info(f"Ses dosyası oluşturuldu: {save_path}")
        
        if play:
            self.play_audio(save_path)
        
        return save_path
    
    def play_audio(self, audio_path: str):
        """Ses dosyasını oynat"""
        if not HAS_PYGAME:
            logger.warning("pygame yüklü değil, ses oynatılamıyor. macOS'ta 'afplay' komutu kullanılıyor")
            # macOS'ta afplay komutu ile ses çal
            try:
                import subprocess
                subprocess.run(['afplay', audio_path], check=True)
                logger.info("Ses oynatma tamamlandı (afplay)")
            except Exception as e:
                logger.error(f"afplay ile ses oynatma hatası: {e}")
            return
        
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            logger.info("Ses oynatma tamamlandı")
        except Exception as e:
            logger.error(f"Ses oynatma hatası: {e}")
    
    def stop_audio(self):
        """Oynatılan sesi durdur"""
        if HAS_PYGAME:
            try:
                pygame.mixer.music.stop()
                logger.info("Ses oynatma durduruldu")
            except Exception as e:
                logger.error(f"Ses durdurma hatası: {e}")
        else:
            logger.warning("pygame mevcut değil, ses durdurma işlemi yapılamıyor")
    
    def speak_code(self, code: str, line_by_line: bool = False):
        """
        Python kodunu sesli olarak oku
        
        Args:
            code: Okunacak kod
            line_by_line: Satır satır okuma modu
        """
        if line_by_line:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip():
                    self.speak(f"Satır {i}: {self._code_to_turkish(line)}")
        else:
            readable_code = self._code_to_turkish(code)
            self.speak(readable_code)
    
    def _code_to_turkish(self, code: str) -> str:
        """
        Python kodunu Türkçe okunabilir hale getir
        
        Args:
            code: Python kodu
        
        Returns:
            str: Türkçeleştirilmiş kod açıklaması
        """
        replacements = {
            'print': 'yazdır',
            'input': 'girdi al',
            'if': 'eğer',
            'else': 'değilse',
            'elif': 'değilse eğer',
            'for': 'for döngüsü',
            'while': 'while döngüsü',
            'def': 'fonksiyon tanımla',
            'class': 'sınıf tanımla',
            'return': 'döndür',
            'import': 'içe aktar',
            '=': 'eşittir',
            '==': 'eşit mi',
            '!=': 'eşit değil mi',
            '+': 'artı',
            '-': 'eksi',
            '*': 'çarpı',
            '/': 'bölü',
        }
        
        result = code
        for eng, tr in replacements.items():
            result = result.replace(eng, tr)
        
        return result


# Test için
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Merhaba, ben Be My Code asistan programıyım.")
