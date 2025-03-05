#!/usr/bin/env python3
"""
Punto de entrada principal para el proyecto de transcripción de Vimeo.
"""
import os
import sys
import argparse
import logging
from pathlib import Path

# Asegurar que los módulos del proyecto son importables
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from src.utils import setup_logger, Timer
from src.downloader import VimeoDownloader
from src.transcriber import WhisperTranscriber

def parse_arguments():
    """Procesa los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Descarga y transcribe videos de Vimeo"
    )
    parser.add_argument(
        "--url", "-u",
        help="URL de Vimeo para descargar (si no se especifica, se leen del archivo)"
    )
    parser.add_argument(
        "--url-file", "-f",
        default=str(settings.URL_FILE),
        help=f"Archivo con URLs de Vimeo (por defecto: {settings.URL_FILE})"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["tiny", "base", "small", "medium", "large"],
        default=settings.WHISPER_MODEL,
        help=f"Modelo de Whisper a utilizar (por defecto: {settings.WHISPER_MODEL})"
    )
    parser.add_argument(
        "--language", "-l",
        default=settings.DEFAULT_LANGUAGE,
        help=f"Idioma para la transcripción (por defecto: {settings.DEFAULT_LANGUAGE})"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=str(settings.TRANSCRIPTION_DIR),
        help=f"Directorio de salida para las transcripciones (por defecto: {settings.TRANSCRIPTION_DIR})"
    )
    parser.add_argument(
        "--keep-audio", "-k",
        action="store_true",
        help="No eliminar los archivos de audio después de la transcripción"
    )
    parser.add_argument(
        "--download-only", "-d",
        action="store_true",
        help="Solo descargar el audio, no transcribir"
    )
    parser.add_argument(
        "--transcribe-only", "-t",
        action="store_true",
        help="Solo transcribir archivos de audio existentes, no descargar"
    )
    
    return parser.parse_args()

def read_urls(file_path):
    """Lee las URLs de un archivo."""
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        logger.error(f"Error al leer el archivo de URLs: {str(e)}")
        return []

def process_single_url(url, args):
    """Procesa una única URL de Vimeo."""
    downloader = VimeoDownloader()
    transcriber = WhisperTranscriber(model_name=args.model, language=args.language)
    
    # Descargar el audio
    audio_file = downloader.download_audio(url)
    if not audio_file:
        logger.error(f"No se pudo descargar el audio de: {url}")
        return False
    
    # Si solo queremos descargar, terminamos aquí
    if args.download_only:
        logger.info(f"Audio descargado correctamente: {audio_file}")
        return True
    
    # Transcribir el audio
    transcription = transcriber.transcribe(
        audio_file, 
        output_dir=args.output_dir
    )
    
    # Eliminar el audio si no se debe conservar
    if not args.keep_audio:
        os.remove(audio_file)
        logger.info(f"Archivo de audio eliminado: {audio_file}")
    
    if transcription:
        logger.info(f"Transcripción completada y guardada")
        return True
    else:
        logger.error("Error en la transcripción")
        return False

def process_batch(urls, args):
    """Procesa un lote de URLs de Vimeo."""
    downloader = VimeoDownloader()
    transcriber = WhisperTranscriber(model_name=args.model, language=args.language)
    
    # Si solo queremos transcribir archivos existentes
    if args.transcribe_only:
        audio_files = list(Path(settings.AUDIO_DIR).glob(f"*.{settings.AUDIO_CODEC}"))
        if not audio_files:
            logger.error(f"No se encontraron archivos de audio en {settings.AUDIO_DIR}")
            return
        
        logger.info(f"Transcribiendo {len(audio_files)} archivos de audio existentes")
        transcriber.transcribe_batch(
            audio_files,
            output_dir=args.output_dir,
            keep_audio=args.keep_audio
        )
        return
    
    # Descargar todos los audios
    audio_files = downloader.download_batch(urls)
    
    # Si solo queremos descargar, terminamos aquí
    if args.download_only:
        logger.info(f"Se descargaron {len(audio_files)} archivos de audio")
        return
    
    # Transcribir todos los audios
    if audio_files:
        transcriber.transcribe_batch(
            audio_files,
            output_dir=args.output_dir,
            keep_audio=args.keep_audio
        )
    else:
        logger.warning("No hay archivos de audio para transcribir")

def main():
    """Función principal."""
    # Configurar el logger
    global logger
    logger = setup_logger()
    
    # Procesar argumentos
    args = parse_arguments()
    
    # Iniciar el cronómetro para todo el proceso
    with Timer("Proceso completo"):
        if args.url:
            # Procesar una única URL
            process_single_url(args.url, args)
        else:
            # Procesar URLs desde un archivo
            urls = read_urls(args.url_file)
            if not urls:
                logger.error(f"No se encontraron URLs en {args.url_file}")
                return
            
            logger.info(f"Se procesarán {len(urls)} URLs de Vimeo")
            process_batch(urls, args)
    
    logger.info("Proceso completado")

if __name__ == "__main__":
    main()