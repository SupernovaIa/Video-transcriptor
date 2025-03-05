"""
Módulo para transcribir audio usando Whisper.
"""
import os
import json
import logging
import whisper
from pathlib import Path

from config import settings
from src.utils import Timer

logger = logging.getLogger("vimeo_transcriber")

class WhisperTranscriber:
    """Clase para gestionar la transcripción de audio con Whisper."""
    
    def __init__(self, model_name=None, language=None):
        """
        Inicializa el transcriptor.
        
        Args:
            model_name: Nombre del modelo de Whisper a usar
            language: Código de idioma para la transcripción
        """
        self.model_name = model_name or settings.WHISPER_MODEL
        self.language = language or settings.DEFAULT_LANGUAGE
        self.model = None
        
    def load_model(self):
        """Carga el modelo de Whisper."""
        if self.model is None:
            logger.info(f"Cargando modelo Whisper: {self.model_name}")
            with Timer("Carga de modelo"):
                self.model = whisper.load_model(self.model_name)
            logger.info("Modelo Whisper cargado correctamente")
        return self.model
        
    def transcribe(self, audio_file, output_dir=None):
        """
        Transcribe un archivo de audio.
        
        Args:
            audio_file: Ruta al archivo de audio
            output_dir: Directorio donde guardar la transcripción (opcional)
            
        Returns:
            Diccionario con información de la transcripción, incluyendo:
            - text: El texto completo
            - segments: Los segmentos individuales con timestamps
            - output_files: Rutas a los archivos de salida
        """
        # Verificar que el archivo existe
        audio_path = Path(audio_file)
        if not audio_path.exists():
            logger.error(f"El archivo de audio no existe: {audio_file}")
            return None
            
        # Usar el directorio especificado o el predeterminado
        output_dir = Path(output_dir) if output_dir else settings.TRANSCRIPTION_DIR
        
        # Crear nombre base para archivos de salida
        base_name = audio_path.stem
        txt_file = output_dir / f"{base_name}.txt"
        json_file = output_dir / f"{base_name}.json"
        vtt_file = output_dir / f"{base_name}.vtt"
        srt_file = output_dir / f"{base_name}.srt"
        
        # Cargar el modelo si no se ha hecho
        self.load_model()
        
        # Transcribir el audio
        logger.info(f"Iniciando transcripción de: {audio_file}")
        with Timer("Transcripción"):
            transcription = self.model.transcribe(
                str(audio_path),
                language=self.language,
                verbose=False
            )
        
        logger.info(f"Transcripción completada: {len(transcription['text'])} caracteres")
        
        # Guardar transcripción en formato texto plano
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(transcription["text"])
        
        # Guardar transcripción completa en JSON para procesamiento posterior
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(transcription, f, ensure_ascii=False, indent=2)
        
        # Guardar transcripción en formato VTT (Web Video Text Tracks)
        self._save_vtt(transcription, vtt_file)
        
        # Guardar transcripción en formato SRT (SubRip)
        self._save_srt(transcription, srt_file)
        
        # Añadir rutas de archivos a los resultados
        transcription["output_files"] = {
            "txt": str(txt_file),
            "json": str(json_file),
            "vtt": str(vtt_file),
            "srt": str(srt_file)
        }
        
        logger.info(f"Archivos guardados en: {output_dir}")
        return transcription
        
    def _save_vtt(self, transcription, vtt_file):
        """Guarda la transcripción en formato VTT."""
        with open(vtt_file, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in transcription["segments"]:
                start_time = self._format_timestamp(segment["start"])
                end_time = self._format_timestamp(segment["end"])
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    def _save_srt(self, transcription, srt_file):
        """Guarda la transcripción en formato SRT."""
        with open(srt_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(transcription["segments"], 1):
                start_time = self._format_timestamp(segment["start"], ms_delimiter=",")
                end_time = self._format_timestamp(segment["end"], ms_delimiter=",")
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    def _format_timestamp(self, seconds, ms_delimiter="."):
        """
        Formatea un tiempo en segundos a formato HH:MM:SS.mmm.
        
        Args:
            seconds: Tiempo en segundos
            ms_delimiter: Delimitador para milisegundos (. para VTT, , para SRT)
        """
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace(".", ms_delimiter)
        
    def transcribe_batch(self, audio_files, output_dir=None, keep_audio=False):
        """
        Transcribe múltiples archivos de audio.
        
        Args:
            audio_files: Lista de rutas a archivos de audio
            output_dir: Directorio donde guardar las transcripciones
            keep_audio: Si es False, elimina los archivos de audio después de transcribirlos
            
        Returns:
            Lista de diccionarios con información de las transcripciones
        """
        results = []
        failed_files = []
        
        for i, audio_file in enumerate(audio_files, 1):
            logger.info(f"Transcribiendo archivo {i}/{len(audio_files)}: {audio_file}")
            
            try:
                transcription = self.transcribe(audio_file, output_dir)
                if transcription:
                    results.append(transcription)
                    
                    # Eliminar el archivo de audio si no se debe conservar
                    if not keep_audio:
                        os.remove(audio_file)
                        logger.info(f"Archivo de audio eliminado: {audio_file}")
                else:
                    failed_files.append(audio_file)
            except Exception as e:
                logger.error(f"Error al transcribir {audio_file}: {str(e)}")
                failed_files.append(audio_file)
                
        # Registrar resultados
        if failed_files:
            logger.warning(f"No se pudieron transcribir {len(failed_files)} archivos")
            for file in failed_files:
                logger.warning(f"  - {file}")
        
        logger.info(f"Transcritos {len(results)} de {len(audio_files)} archivos")
        return results