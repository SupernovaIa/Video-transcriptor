"""
Utilidades para el proyecto de transcripción de Vimeo.
"""
import logging
import time
from datetime import datetime
from pathlib import Path

from config import settings

def setup_logger():
    """Configura y devuelve un logger configurado."""
    # Crear un nombre de archivo basado en la fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = settings.LOGS_DIR / f"vimeo_transcriber_{timestamp}.log"
    
    # Configurar el logger
    logger = logging.getLogger("vimeo_transcriber")
    logger.setLevel(logging.INFO)
    
    # Crear un handler para la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Crear un handler para el archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Registrar todo en el archivo
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Añadir los handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_safe_filename(title):
    """
    Convierte un título en un nombre de archivo seguro.
    Elimina caracteres no seguros y limita la longitud.
    """
    # Caracteres no válidos para nombres de archivo
    invalid_chars = '<>:"/\\|?*'
    
    # Reemplazar caracteres no válidos por guiones bajos
    safe_title = ''.join(c if c not in invalid_chars else '_' for c in title)
    
    # Limitar la longitud del nombre
    if len(safe_title) > 200:
        safe_title = safe_title[:197] + '...'
        
    return safe_title

class Timer:
    """Clase para medir el tiempo de ejecución de bloques de código."""
    
    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        if self.name:
            print(f"{self.name} completado en {elapsed:.2f} segundos")
        return False  # No suprimir excepciones