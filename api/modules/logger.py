"""
Logger modülü - Uygulama genelinde loglama işlemleri
"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name="be_my_code", log_file=None):
    """
    Logger'ı yapılandır
    
    Args:
        name: Logger adı
        log_file: Log dosyası yolu (None ise otomatik oluşturulur)
    
    Returns:
        logging.Logger: Yapılandırılmış logger
    """
    # Vercel serverless environment check
    is_serverless = os.getenv('VERCEL') or os.getenv('AWS_LAMBDA_FUNCTION_NAME')
    
    # Log dizinini oluştur (sadece yazılabilir ortamlarda)
    if not is_serverless:
        try:
            log_dir = Path(__file__).parent.parent.parent / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # Log dosyası adı
            if log_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file = log_dir / f"be_my_code_{timestamp}.log"
        except (OSError, PermissionError):
            # Read-only filesystem, sadece console'a log
            log_file = None
    else:
        # Serverless ortam, dosya loglama yok
        log_file = None
    
    # Logger'ı oluştur
    logger = logging.getLogger(name)
    
    # Eğer daha önce handler eklenmişse, tekrar ekleme
    if logger.handlers:
        return logger
    
    # Log seviyesini ayarla
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(getattr(logging, log_level))
    
    # Formatter oluştur
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (sadece log dosyası varsa)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, IOError):
            # Dosya oluşturulamadıysa sadece console'a log
            pass
    
    # Console handler (her zaman ekle)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
