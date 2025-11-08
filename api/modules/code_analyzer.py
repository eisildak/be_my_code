"""
Kod analiz ve öneri modülü
Jedi kütüphanesi ile kod tamamlama ve analiz
"""

import jedi
from typing import List, Dict, Optional
from modules.logger import setup_logger

logger = setup_logger()


class CodeAnalyzer:
    """Kod analizi ve akıllı öneriler sınıfı"""
    
    def __init__(self):
        logger.info("Kod analiz modülü başlatıldı")
    
    def get_completions(self, code: str, line: int, column: int) -> List[Dict[str, str]]:
        """
        Kod tamamlama önerileri al
        
        Args:
            code: Mevcut kod
            line: Satır numarası (1-indexed)
            column: Sütun numarası (0-indexed)
        
        Returns:
            List[Dict]: Tamamlama önerileri
        """
        try:
            script = jedi.Script(code)
            completions = script.complete(line, column)
            
            results = []
            for comp in completions[:10]:  # İlk 10 öneri
                results.append({
                    'name': comp.name,
                    'type': comp.type,
                    'description': comp.docstring(raw=True)[:100] if comp.docstring() else ""
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Kod tamamlama hatası: {e}")
            return []
    
    def get_definitions(self, code: str, line: int, column: int) -> List[Dict[str, any]]:
        """
        Tanım bilgilerini al (Go to Definition)
        
        Args:
            code: Mevcut kod
            line: Satır numarası
            column: Sütun numarası
        
        Returns:
            List[Dict]: Tanım bilgileri
        """
        try:
            script = jedi.Script(code)
            definitions = script.goto(line, column)
            
            results = []
            for defn in definitions:
                results.append({
                    'name': defn.name,
                    'line': defn.line,
                    'column': defn.column,
                    'module': defn.module_name,
                    'description': defn.docstring(raw=True)[:200] if defn.docstring() else ""
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Tanım arama hatası: {e}")
            return []
    
    def analyze_syntax(self, code: str) -> Dict[str, any]:
        """
        Syntax hatalarını analiz et
        
        Args:
            code: Analiz edilecek kod
        
        Returns:
            Dict: Hata bilgileri
        """
        try:
            script = jedi.Script(code)
            errors = script.get_syntax_errors()
            
            result = {
                'has_errors': len(errors) > 0,
                'errors': []
            }
            
            for error in errors:
                result['errors'].append({
                    'line': error.line,
                    'column': error.column,
                    'message': error.get_message()
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Syntax analiz hatası: {e}")
            return {'has_errors': False, 'errors': []}
    
    def get_context_help(self, code: str, line: int, column: int) -> Optional[str]:
        """
        Bağlamsal yardım al (hover bilgisi)
        
        Args:
            code: Kod
            line: Satır
            column: Sütun
        
        Returns:
            str: Yardım metni veya None
        """
        try:
            script = jedi.Script(code)
            helps = script.help(line, column)
            
            if helps:
                help_text = helps[0].docstring(raw=True)
                return help_text[:500]  # İlk 500 karakter
            
            return None
            
        except Exception as e:
            logger.error(f"Yardım alma hatası: {e}")
            return None


# Test için
if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    
    test_code = """
import os

def hello(name):
    print(f"Hello {name}")
    
hello("World")
os.
"""
    
    # Tamamlama önerileri (os. sonrası)
    completions = analyzer.get_completions(test_code, 8, 3)
    print("Tamamlama önerileri:")
    for comp in completions:
        print(f"  - {comp['name']} ({comp['type']})")
    
    # Syntax kontrolü
    syntax = analyzer.analyze_syntax(test_code)
    print(f"\nSyntax hataları: {syntax}")
