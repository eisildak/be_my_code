"""
Ses tanıma modülü - Kullanıcının sesli komutlarını algılar
SpeechRecognition kütüphanesi ile Türkçe ses tanıma
"""

import speech_recognition as sr
import os
from typing import Optional, Callable
import threading
from modules.logger import setup_logger

logger = setup_logger()


class SpeechRecognizer:
    """Ses tanıma sınıfı"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Ayarlar
        self.language = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "tr-TR")
        self.energy_threshold = int(os.getenv("SPEECH_RECOGNITION_ENERGY_THRESHOLD", "4000"))
        
        # Recognizer ayarları
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Mikrofonu kalibre et
        self._calibrate_microphone()
        
        logger.info("Ses tanıma modülü başlatıldı")
    
    def _calibrate_microphone(self):
        """Mikrofonu ortam gürültüsüne göre kalibre et"""
        try:
            with self.microphone as source:
                logger.info("Mikrofonlar kalibre ediliyor... (Lütfen sessiz olun)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info(f"Kalibrasyon tamamlandı. Enerji eşiği: {self.recognizer.energy_threshold}")
        except Exception as e:
            logger.error(f"Mikrofon kalibrasyonu hatası: {e}")
    
    def listen_once(self, timeout: int = 10, phrase_time_limit: int = 15) -> Optional[str]:
        """
        Bir kez dinle ve metne çevir
        
        Args:
            timeout: Konuşma başlayana kadar bekleme süresi (saniye)
            phrase_time_limit: Maksimum konuşma süresi (saniye)
        
        Returns:
            str: Tanınan metin veya None
        """
        try:
            with self.microphone as source:
                logger.info(f"🎤 Dinleniyor... (timeout: {timeout}s, max konuşma: {phrase_time_limit}s)")
                print(f"🎤 MİKROFON DİNLİYOR - Konuşabilirsiniz...")  # Kullanıcıya görünür mesaj
                
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.info("🔍 Ses tanınıyor (Google API)...")
                print("🔍 Ses tanınıyor, lütfen bekleyin...")
                
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"✅ Tanınan metin: {text}")
                print(f"✅ Tanındı: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("⏱️ Zaman aşımı: Ses algılanamadı")
            print(f"⏱️ ZAMAN AŞIMI - {timeout} saniye içinde ses algılanamadı")
            return None
        except sr.UnknownValueError:
            logger.warning("❓ Ses anlaşılamadı")
            print("❓ Ses anlaşılamadı, lütfen tekrar deneyin")
            return None
        except sr.RequestError as e:
            logger.error(f"🌐 Google Speech Recognition servisi hatası: {e}")
            print(f"🌐 İnternet bağlantısı hatası: {e}")
            return None
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {e}")
            return None
    
    def listen_continuous(self, callback: Callable[[str], None], stop_event: threading.Event):
        """
        Sürekli dinleme modu
        
        Args:
            callback: Tanınan metin için çağrılacak fonksiyon
            stop_event: Dinlemeyi durdurmak için event
        """
        logger.info("Sürekli dinleme modu başlatıldı")
        
        with self.microphone as source:
            while not stop_event.is_set():
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    
                    # Arka planda tanıma yap
                    def recognize_thread():
                        try:
                            text = self.recognizer.recognize_google(audio, language=self.language)
                            logger.info(f"Tanınan metin: {text}")
                            callback(text)
                        except sr.UnknownValueError:
                            pass
                        except Exception as e:
                            logger.error(f"Tanıma hatası: {e}")
                    
                    threading.Thread(target=recognize_thread, daemon=True).start()
                    
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Dinleme hatası: {e}")
                    break
        
        logger.info("Sürekli dinleme modu durduruldu")
    
    def test_microphone(self) -> bool:
        """
        Mikrofon çalışıyor mu test et
        
        Returns:
            bool: Mikrofon çalışıyorsa True
        """
        try:
            logger.info("🎙️ Mikrofon testi başlatılıyor...")
            print("\n" + "="*50)
            print("🎙️ MİKROFON TESTİ")
            print("="*50)
            
            with self.microphone as source:
                print("📊 Ortam gürültüsü ölçülüyor...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print(f"✅ Enerji eşiği: {self.recognizer.energy_threshold}")
                
                print("\n🎤 5 saniye konuşun:")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                
                print("🔍 Ses tanınıyor...")
                text = self.recognizer.recognize_google(audio, language=self.language)
                
                print(f"✅ BAŞARILI! Tanınan: '{text}'")
                print("="*50 + "\n")
                
                logger.info(f"Mikrofon testi başarılı: {text}")
                return True
                
        except Exception as e:
            print(f"❌ HATA: {e}")
            print("="*50 + "\n")
            logger.error(f"Mikrofon testi başarısız: {e}")
            return False


# Test için
if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    
    if recognizer.test_microphone():
        print("Bir şey söyleyin...")
        text = recognizer.listen_once()
        if text:
            print(f"Tanınan: {text}")
        else:
            print("Ses tanınamadı")
