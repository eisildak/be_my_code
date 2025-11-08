"""
Gemini AI Kod Üretici Modülü
Google Gemini API ile Türkçe komutları Python koduna çevirir
"""

import os
import google.generativeai as genai
from typing import Optional
from modules.logger import setup_logger

logger = setup_logger()


class GeminiCodeGenerator:
    """Google Gemini AI kullanarak akıllı kod üretir"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Gemini API anahtarı (opsiyonel, environment'tan alınabilir)
        """
        self.model = None
        self.api_key = api_key
        
        # API key kontrolü
        if not api_key:
            # Environment variable'dan oku (Vercel için)
            api_key = os.getenv('GEMINI_API_KEY')
            
            # Eğer hala yoksa .env'den dene (lokal development için)
            if not api_key:
                try:
                    from dotenv import load_dotenv
                    load_dotenv()
                    api_key = os.getenv('GEMINI_API_KEY')
                except:
                    pass
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini AI başarıyla yapılandırıldı")
            except Exception as e:
                logger.error(f"Gemini yapılandırma hatası: {e}")
                self.model = None
        else:
            logger.warning("Gemini API key bulunamadı. .env dosyasına GEMINI_API_KEY ekleyin")
    
    def is_available(self) -> bool:
        """Gemini kullanılabilir mi?"""
        return self.model is not None
    
    def generate_code(self, command: str, context: Optional[str] = None) -> Optional[str]:
        """
        Türkçe komuttan Python kodu üret
        
        Args:
            command: Türkçe sesli komut
            context: Mevcut kod bağlamı (son birkaç satır)
        
        Returns:
            str: Üretilen Python kodu veya None
        """
        if not self.is_available():
            logger.warning("Gemini kullanılamıyor")
            return None
        
        try:
            # Prompt hazırla
            prompt = self._create_code_generation_prompt(command, context)
            
            # Gemini'den kod üret
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Daha deterministik
                    max_output_tokens=500,
                )
            )
            
            # Kodu çıkar
            code = self._extract_code(response.text)
            
            if code:
                logger.info(f"Gemini kod üretti: {code[:50]}...")
                return code
            else:
                logger.warning("Gemini'den geçerli kod çıkarılamadı")
                return None
                
        except Exception as e:
            logger.error(f"Gemini kod üretme hatası: {e}")
            return None
    
    def explain_error(self, error: str, code: str) -> Optional[str]:
        """
        Python hatasını Türkçe açıkla ve düzeltme öner
        
        Args:
            error: Hata mesajı
            code: Hatalı kod
        
        Returns:
            str: Türkçe açıklama ve öneri
        """
        if not self.model:
            return None
        
        try:
            prompt = f"""
Python hatası aldım. Bunu basit Türkçe açıkla ve nasıl düzelteceğimi söyle.

HATA:
{error}

KOD:
{code}

Açıklama ve çözüm (kısa ve öz):
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Hata açıklama hatası: {e}")
            return None


# Test için
if __name__ == "__main__":
    import sys
    
    # API key kontrolü
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY bulunamadı!")
        print("Çözüm: .env dosyasına ekleyin:")
        print("  GEMINI_API_KEY=your_api_key_here")
        print("\nAPI key almak için: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    # Test
    generator = GeminiCodeGenerator()
    
    if generator.is_available():
        print("✅ Gemini hazır!\n")
        
        # Test komutları
        test_commands = [
            "isim adında string değişken oluştur",
            "1'den 10'a kadar sayıları yazdır",
            "kullanıcıdan yaş al ve ekrana yazdır",
            "faktöriyel hesaplayan fonksiyon yaz"
        ]
        
        for cmd in test_commands:
            print(f"Komut: {cmd}")
            code = generator.generate_code(cmd)
            if code:
                print(f"Kod:\n{code}\n")
            else:
                print("Kod üretilemedi\n")
    else:
        print("❌ Gemini başlatılamadı!")
