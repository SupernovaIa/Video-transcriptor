# Vimeo Transcriber

Un proyecto completo para descargar el audio de videos de Vimeo y transcribirlo utilizando el modelo Whisper de OpenAI.

## Características

- ✅ Descarga de audio de videos de Vimeo mediante yt-dlp
- ✅ Transcripción automática utilizando el modelo Whisper de OpenAI
- ✅ Generación de transcripciones en múltiples formatos (TXT, JSON, VTT, SRT)
- ✅ Soporte para procesar lotes de URLs
- ✅ Sistema de registro detallado de operaciones
- ✅ Interfaz de línea de comandos flexible
- ✅ Configuración centralizada y personalizable

## Requisitos

- Python 3.7 o superior
- FFmpeg (para procesamiento de audio)
- GPU recomendada para transcripciones más rápidas (opcional)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/vimeo-transcriber.git
cd vimeo-transcriber
```

2. Crea un entorno virtual e instala las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Instala FFmpeg:

   - **Ubuntu/Debian**:
     ```bash
     sudo apt update && sudo apt install ffmpeg
     ```
   
   - **Windows**: Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y añade al PATH
   
   - **macOS**:
     ```bash
     brew install ffmpeg
     ```

## Uso

### Modo básico

1. Coloca las URLs de Vimeo en el archivo `data/urls.txt`, una URL por línea.
2. Ejecuta el script principal:

```bash
python main.py
```

### Opciones avanzadas

```bash
# Procesar una sola URL
python main.py --url https://vimeo.com/XXXXXXXX/YYYYYYYY

# Usar un modelo específico de Whisper
python main.py --model medium

# Especificar el idioma de la transcripción
python main.py --language es

# Mantener los archivos de audio después de la transcripción
python main.py --keep-audio

# Solo descargar, sin transcribir
python main.py --download-only

# Solo transcribir archivos existentes, sin descargar
python main.py --transcribe-only

# Ver todas las opciones disponibles
python main.py --help
```

## Estructura de archivos generados

Por cada video procesado, el sistema genera:

- `transcriptions/nombre_del_video.txt` - Texto plano
- `transcriptions/nombre_del_video.json` - Formato JSON con metadatos
- `transcriptions/nombre_del_video.vtt` - Formato WebVTT para subtítulos web
- `transcriptions/nombre_del_video.srt` - Formato SubRip para subtítulos

## Modelos de Whisper disponibles

| Modelo  | Precisión | Velocidad | Memoria requerida |
|---------|-----------|-----------|-------------------|
| tiny    | Baja      | Muy rápido| ~1GB              |
| base    | Básica    | Rápido    |