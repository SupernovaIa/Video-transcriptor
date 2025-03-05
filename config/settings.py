"""
Configuraciones centralizadas para el proyecto de transcripción de Vimeo.
"""
import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Rutas de datos
AUDIO_DIR = DATA_DIR / "audios"
TRANSCRIPTION_DIR = DATA_DIR / "transcriptions"
URL_FILE = DATA_DIR / "urls.txt"

# Configuración de Whisper
WHISPER_MODEL = "base"  # opciones: "tiny", "base", "small", "medium", "large"
DEFAULT_LANGUAGE = "es"  # Idioma por defecto para la transcripción

# Configuración de yt-dlp
AUDIO_FORMAT = "bestaudio"
AUDIO_CODEC = "mp3"
AUDIO_QUALITY = "192"

# Crear directorios necesarios
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)