"""
NLP (Doğal Dil İşleme) Modülü
Sesli komutları Python koduna çevirir
"""

import re
from typing import Optional, Dict, List
from modules.logger import setup_logger

logger = setup_logger()

# Gemini'yi yükle (opsiyonel)
try:
    from modules.gemini_code_generator import GeminiCodeGenerator
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    logger.warning("Gemini modülü yüklenemedi, basit NLP kullanılacak")


class NLPProcessor:
    """Doğal dil komutlarını Python koduna çeviren sınıf"""
    
    def __init__(self):
        self.command_patterns = self._initialize_patterns()
        
        # Gemini'yi başlat (varsa)
        self.gemini = None
        if HAS_GEMINI:
            try:
                self.gemini = GeminiCodeGenerator()
                if self.gemini.is_available():
                    logger.info("NLP modülü Gemini AI ile başlatıldı (Akıllı mod)")
                else:
                    logger.info("NLP modülü basit mod ile başlatıldı (Gemini API key yok)")
                    self.gemini = None
            except Exception as e:
                logger.warning(f"Gemini başlatılamadı: {e}, basit mod kullanılacak")
                self.gemini = None
        else:
            logger.info("NLP modülü başlatıldı (Basit mod)")
    
    def _initialize_patterns(self) -> Dict[str, callable]:
        """
        Komut patternlerini ve işleyicilerini tanımla
        
        Returns:
            Dict: Komut pattern'leri ve işleyici fonksiyonları
        """
        return {
            # Değişken tanımlama
            r'(string|metin|text)\s+(değişken|degisken)?\s*(\w+)?': self._create_string_variable,
            r'(integer|int|sayı|sayi|tam sayı)\s+(değişken|degisken)?\s*(\w+)?': self._create_int_variable,
            r'(float|ondalık|ondalik)\s+(değişken|degisken)?\s*(\w+)?': self._create_float_variable,
            r'(boolean|bool)\s+(değişken|degisken)?\s*(\w+)?': self._create_bool_variable,
            r'(list|liste)\s+(değişken|degisken)?\s*(\w+)?': self._create_list_variable,
            
            # Döngüler
            r'for\s+(döngü|dongu|döngüsü|dongusu)(\s+yaz)?': self._create_for_loop,
            r'while\s+(döngü|dongu|döngüsü|dongusu)(\s+yaz)?': self._create_while_loop,
            
            # Koşullar
            r'if\s+(koşul|kosul|koşulu|kosulu)?(\s+yaz)?': self._create_if_statement,
            
            # Fonksiyon
            r'(fonksiyon|function)\s+(tanımla|tanimla)?(\s+\w+)?': self._create_function,
            
            # Print
            r'(yazdır|yazdir|print)': self._create_print,
            
            # Input
            r'(girdi|input)\s*(al)?': self._create_input,
            
            # Yorum
            r'(yorum|comment)\s+(.+)': self._create_comment,
        }
    
    def process_command(self, command: str, context: str = "") -> Optional[str]:
        """
        Ses komutunu Python koduna çevir
        
        Args:
            command: Kullanıcının sesli komutu
            context: Mevcut kod bağlamı (Gemini için)
        
        Returns:
            str: Python kodu veya None
        """
        command = command.lower().strip()
        logger.info(f"Komut işleniyor: {command}")
        
        # Önce basit pattern'leri dene (hızlı)
        for pattern, handler in self.command_patterns.items():
            match = re.search(pattern, command)
            if match:
                try:
                    code = handler(match, command)
                    logger.info(f"Kod oluşturuldu (Pattern): {code}")
                    return code
                except Exception as e:
                    logger.error(f"Kod oluşturma hatası: {e}")
                    return None
        
        # Pattern tanımadıysa, Gemini'yi dene
        if self.gemini:
            logger.info("Pattern tanınmadı, Gemini AI devreye giriyor...")
            code = self.gemini.generate_code(command, context)
            if code:
                logger.info(f"Kod oluşturuldu (Gemini): {code[:100]}...")
                return code
        
        logger.warning(f"Komut tanınmadı: {command}")
        return None
    
    # Kod oluşturma fonksiyonları
    
    def _create_string_variable(self, match, command: str) -> str:
        """String değişken oluştur"""
        var_name = self._extract_variable_name(match, command, default="metin")
        return f'{var_name} = ""'
    
    def _create_int_variable(self, match, command: str) -> str:
        """Integer değişken oluştur"""
        var_name = self._extract_variable_name(match, command, default="sayi")
        return f'{var_name} = 0'
    
    def _create_float_variable(self, match, command: str) -> str:
        """Float değişken oluştur"""
        var_name = self._extract_variable_name(match, command, default="ondalik")
        return f'{var_name} = 0.0'
    
    def _create_bool_variable(self, match, command: str) -> str:
        """Boolean değişken oluştur"""
        var_name = self._extract_variable_name(match, command, default="durum")
        return f'{var_name} = False'
    
    def _create_list_variable(self, match, command: str) -> str:
        """Liste değişken oluştur"""
        var_name = self._extract_variable_name(match, command, default="liste")
        return f'{var_name} = []'
    
    def _create_for_loop(self, match, command: str) -> str:
        """For döngüsü oluştur"""
        return """for i in range(10):
    # Kod buraya"""
    
    def _create_while_loop(self, match, command: str) -> str:
        """While döngüsü oluştur"""
        return """while True:
    # Kod buraya
    break"""
    
    def _create_if_statement(self, match, command: str) -> str:
        """If koşulu oluştur"""
        return """if True:
    # Kod buraya
else:
    # Kod buraya"""
    
    def _create_function(self, match, command: str) -> str:
        """Fonksiyon oluştur"""
        func_name = match.group(3) if match.group(3) else "fonksiyon"
        return f"""def {func_name}():
    # Kod buraya
    pass"""
    
    def _create_print(self, match, command: str) -> str:
        """Print komutu oluştur"""
        return 'print("")'
    
    def _create_input(self, match, command: str) -> str:
        """Input komutu oluştur"""
        return 'input("Bir değer girin: ")'
    
    def _create_comment(self, match, command: str) -> str:
        """Yorum satırı oluştur"""
        comment_text = match.group(2)
        return f'# {comment_text}'
    
    def _extract_variable_name(self, match, command: str, default: str = "degisken") -> str:
        """
        Komuttan değişken adını çıkar
        
        Args:
            match: Regex match objesi
            command: Tam komut
            default: Varsayılan değişken adı
        
        Returns:
            str: Değişken adı
        """
        # Match'ten değişken adı al
        if match.lastindex and match.lastindex >= 3:
            var_name = match.group(3)
            if var_name:
                return var_name
        
        # Komuttan "adı X" veya "ismi X" şeklinde ara
        name_patterns = [
            r'(adı|adi|ismi|isim)\s+(\w+)',
            r'(\w+)\s+(adında|adinda|isimli|isminde)',
        ]
        
        for pattern in name_patterns:
            name_match = re.search(pattern, command)
            if name_match:
                return name_match.group(2) if '|' in pattern else name_match.group(1)
        
        return default
    
    def get_suggestions(self, context: str) -> List[str]:
        """
        Bağlama göre kod önerileri ver
        
        Args:
            context: Mevcut kod bağlamı
        
        Returns:
            List[str]: Öneri listesi
        """
        suggestions = []
        
        # For döngüsü içinde
        if 'for' in context.lower() and 'range' in context.lower():
            suggestions.extend([
                "print ile değer yazdırabilirsiniz",
                "liste.append ile eleman ekleyebilirsiniz",
                "if koşulu ekleyebilirsiniz"
            ])
        
        # While döngüsü içinde
        elif 'while' in context.lower():
            suggestions.extend([
                "break ile döngüden çıkabilirsiniz",
                "continue ile bir sonraki iterasyona geçebilirsiniz",
                "if koşulu ile kontrol ekleyebilirsiniz"
            ])
        
        # If koşulu içinde
        elif 'if' in context.lower():
            suggestions.extend([
                "else bloğu ekleyebilirsiniz",
                "elif ile başka koşul ekleyebilirsiniz"
            ])
        
        # Genel öneriler
        else:
            suggestions.extend([
                "for döngüsü yazabilirsiniz",
                "while döngüsü yazabilirsiniz",
                "fonksiyon tanımlayabilirsiniz",
                "değişken oluşturabilirsiniz"
            ])
        
        return suggestions


# Test için
if __name__ == "__main__":
    nlp = NLPProcessor()
    
    test_commands = [
        "string değişken yaz",
        "integer değişken adı sayı",
        "for döngüsü yaz",
        "while döngüsü oluştur",
        "if koşulu",
        "fonksiyon tanımla hesapla",
        "yazdır",
        "yorum bu bir test yorumu"
    ]
    
    for cmd in test_commands:
        print(f"\nKomut: {cmd}")
        code = nlp.process_command(cmd)
        if code:
            print(f"Kod:\n{code}")
        else:
            print("Kod oluşturulamadı")
