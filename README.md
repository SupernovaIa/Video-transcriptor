# Vimeo Transcriber

Vimeo Transcriber es una herramienta que facilita la descarga y transcripción automática del audio de videos alojados en Vimeo, utilizando el potente modelo Whisper de OpenAI. Ideal para usuarios que necesiten generar subtítulos o texto a partir de videos de forma sencilla y eficiente.

## 📌 Características principales

- ✅ Descarga automática del audio de videos en Vimeo con **yt-dlp**.
- ✅ Transcripción precisa mediante el modelo Whisper de OpenAI.
- ✅ Soporte para múltiples formatos de salida: TXT, JSON, VTT y SRT.
- ✅ Procesamiento de múltiples URLs simultáneamente.
- ✅ Registro detallado (logs) de todas las operaciones.
- ✅ Interfaz de línea de comandos intuitiva y flexible.
- ✅ Configuración centralizada y fácil de personalizar.

## 🚀 Requisitos

- **Python 3.7** o superior
- **FFmpeg** (necesario para el procesamiento del audio)
- GPU opcional, pero recomendada para transcripciones más rápidas

## ⚙️ Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu-usuario/vimeo-transcriber.git
cd vimeo-transcriber
```

2. **Configura un entorno virtual e instala dependencias:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Instala FFmpeg:**

- **Ubuntu/Debian:**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

- **Windows:** Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y añade al PATH.

- **macOS:**
  ```bash
  brew install ffmpeg
  ```

## 🎯 Uso

### 🔹 Modo básico

1. Agrega las URLs de Vimeo en `data/urls.txt`, una por línea.
2. Ejecuta la herramienta:

```bash
python main.py
```

### 🔸 Opciones avanzadas

```bash
# Procesar una URL específica
python main.py --url https://vimeo.com/XXXXXXXX/YYYYYYYY

# Seleccionar un modelo Whisper específico
python main.py --model medium

# Especificar idioma de la transcripción
python main.py --language es

# Conservar archivos de audio después de transcribir
python main.py --keep-audio

# Solo descargar audio sin transcribir
python main.py --download-only

# Transcribir archivos ya descargados
python main.py --transcribe-only

# Consultar ayuda detallada
python main.py --help
```

## 📂 Archivos generados

Para cada video procesado, se generan automáticamente:

- `transcriptions/<nombre_del_video>.txt` – Texto plano
- `transcriptions/<nombre_del_video>.json` – JSON con metadatos
- `transcriptions/<nombre_del_video>.vtt` – Subtítulos en formato WebVTT
- `transcriptions/<nombre_del_video>.srt` – Subtítulos en formato SubRip

## 🧠 Modelos Whisper disponibles

| Modelo  | Precisión | Velocidad | Memoria requerida |
|---------|-----------|-----------|-------------------|
| tiny    | Baja      | Muy rápido| ~1 GB             |
| base    | Básica    | Rápido    | ~1 GB             |
| small   | Moderada  | Moderado  | ~2 GB             |
| medium  | Alta      | Lento     | ~5 GB             |
| large   | Muy Alta  | Muy lento | ~10 GB            |

