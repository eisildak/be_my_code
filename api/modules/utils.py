"""
Yardımcı fonksiyonlar ve araçlar
"""

import os
import subprocess
from typing import Optional
from pathlib import Path


def run_python_code(code: str, timeout: int = 30) -> tuple[str, str, int]:
    """
    Python kodunu güvenli bir şekilde çalıştır
    
    Args:
        code: Çalıştırılacak Python kodu
        timeout: Zaman aşımı (saniye)
    
    Returns:
        tuple: (stdout, stderr, return_code)
    """
    try:
        # Geçici dosya oluştur
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Kodu çalıştır
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Geçici dosyayı sil
        os.unlink(temp_file)
        
        return result.stdout, result.stderr, result.returncode
        
    except subprocess.TimeoutExpired:
        return "", "Zaman aşımı: Kod çok uzun süre çalıştı", 1
    except Exception as e:
        return "", f"Hata: {str(e)}", 1


def format_code(code: str) -> str:
    """
    Python kodunu biçimlendir (black kullanarak)
    
    Args:
        code: Biçimlendirilecek kod
    
    Returns:
        str: Biçimlendirilmiş kod
    """
    try:
        import black
        mode = black.Mode()
        formatted = black.format_str(code, mode=mode)
        return formatted
    except Exception:
        # black yoksa veya hata varsa, orijinal kodu döndür
        return code


def check_syntax(code: str) -> tuple[bool, Optional[str]]:
    """
    Python kodunun syntax'ını kontrol et
    
    Args:
        code: Kontrol edilecek kod
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        compile(code, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        error_msg = f"Satır {e.lineno}: {e.msg}"
        return False, error_msg
    except Exception as e:
        return False, str(e)


def get_file_extension(filename: str) -> str:
    """
    Dosya uzantısını al
    
    Args:
        filename: Dosya adı
    
    Returns:
        str: Dosya uzantısı (nokta ile)
    """
    return Path(filename).suffix


def is_python_file(filename: str) -> bool:
    """
    Dosyanın Python dosyası olup olmadığını kontrol et
    
    Args:
        filename: Dosya adı
    
    Returns:
        bool: Python dosyası ise True
    """
    return get_file_extension(filename).lower() == '.py'


def count_lines(code: str) -> int:
    """
    Kod satır sayısını say
    
    Args:
        code: Kod
    
    Returns:
        int: Satır sayısı
    """
    return len(code.split('\n'))


def get_code_stats(code: str) -> dict:
    """
    Kod istatistiklerini al
    
    Args:
        code: Kod
    
    Returns:
        dict: İstatistikler
    """
    lines = code.split('\n')
    
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
    code_lines = total_lines - blank_lines - comment_lines
    
    return {
        'total_lines': total_lines,
        'code_lines': code_lines,
        'blank_lines': blank_lines,
        'comment_lines': comment_lines,
        'characters': len(code)
    }


def sanitize_filename(filename: str) -> str:
    """
    Dosya adını güvenli hale getir
    
    Args:
        filename: Orijinal dosya adı
    
    Returns:
        str: Güvenli dosya adı
    """
    # Geçersiz karakterleri kaldır
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename


# Test için
if __name__ == "__main__":
    test_code = """
def hello():
    print("Hello World")
    
hello()
"""
    
    # Syntax kontrolü
    is_valid, error = check_syntax(test_code)
    print(f"Syntax geçerli: {is_valid}")
    if error:
        print(f"Hata: {error}")
    
    # Kodu çalıştır
    stdout, stderr, code = run_python_code(test_code)
    print(f"\nÇıktı: {stdout}")
    if stderr:
        print(f"Hata: {stderr}")
    
    # İstatistikler
    stats = get_code_stats(test_code)
    print(f"\nİstatistikler: {stats}")
