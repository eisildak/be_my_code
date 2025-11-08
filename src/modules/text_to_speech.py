"""
Text-to-Speech modülü - Coqui-XTTS v2 ile profesyonel Türkçe seslendirme
Yazılan kodları ve mesajları sesli olarak okur
"""

import os
import torch
from TTS.api import TTS
from pathlib import Path
import tempfile
from typing import Optional
import pygame
from modules.logger import setup_logger

logger = setup_logger()


class TextToSpeech:
    """Coqui-XTTS v2 ile text-to-speech sınıfı"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = os.getenv("TTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")
        self.language = os.getenv("TTS_LANGUAGE", "tr")
        
        logger.info(f"TTS modülü başlatılıyor... (Cihaz: {self.device})")
        
        # TTS modelini yükle
        try:
            self.tts = TTS(self.model_name).to(self.device)
            logger.info("Coqui-XTTS v2 modeli başarıyla yüklendi")
        except Exception as e:
            logger.error(f"TTS modeli yüklenemedi: {e}")
            self.tts = None
        
        # Pygame mixer'ı ses çalmak için başlat
        pygame.mixer.init()
        
        # Referans ses dosyası (Türkçe konuşan kişi sesi için)
        self.speaker_wav = self._get_speaker_wav()
    
    def _get_speaker_wav(self) -> Optional[str]:
        """
        Referans konuşmacı ses dosyasını al
        
        Returns:
            str: Ses dosyası yolu veya None
        """
        speaker_path = os.getenv("TTS_SPEAKER_WAV")
        
        if speaker_path and Path(speaker_path).exists():
            logger.info(f"Referans ses dosyası kullanılıyor: {speaker_path}")
            return speaker_path
        
        # Varsayılan referans ses yoksa, model kendi sesini kullanacak
        logger.info("Referans ses dosyası bulunamadı, model varsayılan sesi kullanacak")
        return None
    
    def speak(self, text: str, save_path: Optional[str] = None, play: bool = True) -> Optional[str]:
        """
        Metni seslendir
        
        Args:
            text: Seslendirilecek metin
            save_path: Ses dosyasını kaydetme yolu (None ise geçici dosya)
            play: Ses dosyasını otomatik oynat
        
        Returns:
            str: Oluşturulan ses dosyası yolu veya None
        """
        if not self.tts:
            logger.error("TTS modeli yüklü değil!")
            return None
        
        if not text or text.strip() == "":
            logger.warning("Boş metin seslendirilemez")
            return None
        
        try:
            # Geçici dosya oluştur
            if save_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                save_path = temp_file.name
                temp_file.close()
            
            logger.info(f"Seslendiriliyor: {text[:50]}...")
            
            # XTTS v2 ile seslendirme
            if self.speaker_wav:
                # Referans ses ile klonlama
                self.tts.tts_to_file(
                    text=text,
                    file_path=save_path,
                    speaker_wav=self.speaker_wav,
                    language=self.language
                )
            else:
                # Varsayılan ses ile
                self.tts.tts_to_file(
                    text=text,
                    file_path=save_path,
                    language=self.language
                )
            
            logger.info(f"Ses dosyası oluşturuldu: {save_path}")
            
            # Ses dosyasını oynat
            if play:
                self.play_audio(save_path)
            
            return save_path
            
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
            return None
    
    def play_audio(self, audio_path: str):
        """
        Ses dosyasını oynat
        
        Args:
            audio_path: Oynatılacak ses dosyası yolu
        """
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Ses bitene kadar bekle
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            logger.info("Ses oynatma tamamlandı")
            
        except Exception as e:
            logger.error(f"Ses oynatma hatası: {e}")
    
    def stop_audio(self):
        """Oynatılan sesi durdur"""
        try:
            pygame.mixer.music.stop()
            logger.info("Ses oynatma durduruldu")
        except Exception as e:
            logger.error(f"Ses durdurma hatası: {e}")
    
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
            # Tüm kodu bir arada oku
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
        # Basit Türkçeleştirme (geliştirilecek)
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
            '(': 'parantez aç',
            ')': 'parantez kapat',
            '[': 'köşeli parantez aç',
            ']': 'köşeli parantez kapat',
            '{': 'süslü parantez aç',
            '}': 'süslü parantez kapat',
            ':': 'iki nokta',
        }
        
        result = code
        for eng, tr in replacements.items():
            result = result.replace(eng, tr)
        
        return result


# Test için
if __name__ == "__main__":
    tts = TextToSpeech()
    
    # Test metni
    tts.speak("Merhaba, ben Be My Code asistan programıyım. Size Python kodu yazmanızda yardımcı olacağım.")
    
    # Test kodu
    sample_code = """
x = 10
for i in range(x):
    print(i)
"""
    tts.speak_code(sample_code, line_by_line=True)
