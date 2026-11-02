# Interview Copilot

Copiloto de escritorio para entrevistas de trabajo en inglés. Escucha el audio de la llamada (Zoom, Meet, Teams), transcribe en tiempo real y, cuando detecta una pregunta, sugiere una respuesta basada en el CV de la persona.

> Proyecto personal / portafolio.

## Cómo funciona

```
Audio del sistema ──► Deepgram (STT streaming) ──► Transcripción en vivo
   (WASAPI loopback)                                     │
                                                         ▼
                                            Detección de pregunta completa
                                                         │
                     Knowledge base del CV (Chroma) ◄────┤  RAG
                                                         ▼
                                           Claude API ──► Respuesta sugerida
                                                         │
                                                         ▼
                                       Overlay flotante (PyQt6)
```

1. **Captura de audio**: toma lo que sale por los parlantes (no el micrófono) usando WASAPI loopback.
2. **Transcripción**: envía el audio en streaming a Deepgram.
3. **Detección de pregunta**: identifica cuándo el entrevistador terminó de formular una pregunta.
4. **RAG**: busca los fragmentos más relevantes del CV de la persona en su colección de Chroma.
5. **Respuesta**: Claude genera una respuesta sugerida con la pregunta y ese contexto.
6. **Overlay**: una ventana flotante muestra la transcripción y la respuesta en vivo.

Cada persona tiene su propia knowledge base (una colección de Chroma por persona), así que varias personas pueden usar la app con su propio CV.

## Stack

| Componente        | Tecnología                         |
| ----------------- | ---------------------------------- |
| Lenguaje          | Python 3.11+                       |
| Captura de audio  | PyAudioWPatch (WASAPI loopback)    |
| Speech-to-text    | Deepgram SDK (streaming)           |
| LLM               | Anthropic SDK, Claude Sonnet       |
| Vector store      | Chroma (local, persistente)        |
| Extracción de CV  | pypdf, python-docx                 |
| UI                | PyQt6                              |
| Configuración     | python-dotenv                      |

## Estructura

```
.
├── app/
│   ├── config.py          # .env, rutas y constantes (SAMPLE_RATE, CHUNK_MS, CLAUDE_MODEL)
│   └── audio_capture.py   # list_devices() y stream_system_audio() vía WASAPI loopback
├── cvs/                   # CVs de cada persona (no se versionan)
├── data/
│   └── chroma/            # persistencia del vector store (no se versiona)
├── requirements.txt
└── .env.example
```

## Requisitos

- **Windows 10/11** para la captura de audio (WASAPI loopback). El resto de los módulos (transcripción desde archivo, ingesta de CV, RAG, UI) también funcionan en macOS y Linux para desarrollo.
- Python 3.11 o superior.
- API keys de [Deepgram](https://console.deepgram.com/) y [Anthropic](https://console.anthropic.com/).

## Instalación

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # y completa las API keys
```

`PyAudioWPatch` solo se instala en Windows (está marcado con `sys_platform == "win32"` en `requirements.txt`).

## Configuración

Variables en `.env`:

| Variable            | Descripción                                    |
| ------------------- | ---------------------------------------------- |
| `DEEPGRAM_API_KEY`  | API key de Deepgram                            |
| `ANTHROPIC_API_KEY` | API key de Anthropic                           |
| `CLAUDE_MODEL`      | Opcional. Modelo de Claude (por defecto `claude-sonnet-5-5`) |

## Roadmap

- [x] Estructura del proyecto y configuración
- [ ] Captura de audio del sistema con WASAPI loopback (probar en Windows)
- [ ] Cliente de streaming a Deepgram con transcripción en vivo
- [ ] Ingesta de CV: extracción, chunking, embeddings y una colección de Chroma por persona
- [ ] Detección de preguntas y generación de respuestas con Claude + RAG
- [ ] Overlay UI en PyQt6

## Privacidad

Los CVs y el vector store se guardan solo en local (`cvs/` y `data/chroma/`) y están excluidos de git. Para transcribir y generar respuestas, el audio se envía a Deepgram y las preguntas, junto con fragmentos del CV, a Anthropic.
