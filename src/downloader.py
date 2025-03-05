"""
Módulo para descargar audio de videos de Vimeo.
"""
import os
import re
import yt_dlp
import logging
from pathlib import Path

from config import settings
from src.utils import get_safe_filename, Timer

logger = logging.getLogger("vimeo_transcriber")

class VimeoDownloader:
    """Clase para gestionar la descarga de audio de videos de Vimeo."""
    
    def __init__(self):
        self.download_options = {
            "format": settings.AUDIO_FORMAT,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": settings.AUDIO_CODEC,
                "preferredquality": settings.AUDIO_QUALITY
            }],
            "quiet": False,
            "no_warnings": False,
            "progress_hooks": [self._progress_hook],
        }
    
    def _progress_hook(self, d):
        """Hook para informar sobre el progreso de la descarga."""
        if d['status'] == 'downloading':
            # Mostrar el progreso de manera opcional
            pass
        elif d['status'] == 'finished':
            logger.info(f"Descarga completada: {d['filename']}")
        elif d['status'] == 'error':
            logger.error(f"Error en la descarga: {d.get('error')}")
    
    def validate_vimeo_url(self, url):
        """Valida que la URL sea de Vimeo y tenga el formato correcto."""
        # Patrón para URLs de Vimeo
        pattern = r'^https?://(www\.)?vimeo\.com/(?:\d+)(?:/[a-zA-Z0-9]+)?$'
        return bool(re.match(pattern, url))
    
    def download_audio(self, url, custom_filename=None):
        """
        Descarga el audio de un video de Vimeo.
        
        Args:
            url: URL del video de Vimeo
            custom_filename: Nombre de archivo personalizado (opcional)
            
        Returns:
            Ruta al archivo de audio descargado o None si hay un error
        """
        try:
            # Preparar opciones de descarga
            options = self.download_options.copy()
            
            if custom_filename:
                safe_filename = get_safe_filename(custom_filename)
                output_path = settings.AUDIO_DIR / f"{safe_filename}.%(ext)s"
            else:
                output_path = settings.AUDIO_DIR / "%(title)s.%(ext)s"
            
            options["outtmpl"] = str(output_path)
            
            # Iniciar la descarga
            logger.info(f"Iniciando descarga de: {url}")
            with Timer("Descarga"):
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    # Obtener la ruta del archivo descargado
                    if custom_filename:
                        filename = f"{safe_filename}.{settings.AUDIO_CODEC}"
                    else:
                        title = info.get('title', 'unknown_title')
                        safe_title = get_safe_filename(title)
                        filename = f"{safe_title}.{settings.AUDIO_CODEC}"
                    
                    downloaded_file = settings.AUDIO_DIR / filename
                    
                    # Verificar si el archivo existe
                    if not os.path.exists(downloaded_file):
                        # Buscar el archivo en el directorio
                        audio_files = list(settings.AUDIO_DIR.glob(f"*.{settings.AUDIO_CODEC}"))
                        if audio_files:
                            # Usar el archivo más reciente
                            downloaded_file = max(audio_files, key=os.path.getctime)
                        else:
                            logger.error("No se encontró el archivo descargado")
                            return None
                    
                    logger.info(f"Audio descargado: {downloaded_file}")
                    return downloaded_file
                    
        except Exception as e:
            logger.error(f"Error al descargar audio: {str(e)}")
            return None
            
    def download_batch(self, urls):
        """
        Descarga múltiples videos de Vimeo.
        
        Args:
            urls: Lista de URLs de Vimeo
            
        Returns:
            Lista de rutas a los archivos descargados
        """
        downloaded_files = []
        failed_urls = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Procesando URL {i}/{len(urls)}: {url}")
            audio_file = self.download_audio(url)
            
            if audio_file:
                downloaded_files.append(audio_file)
            else:
                failed_urls.append(url)
                
        # Registrar resultados
        if failed_urls:
            logger.warning(f"No se pudieron descargar {len(failed_urls)} videos")
            for url in failed_urls:
                logger.warning(f"  - {url}")
        
        logger.info(f"Descargados {len(downloaded_files)} de {len(urls)} videos")
        return downloaded_files