# JanSahayak — Exotel Voicebot Audio Pipeline

## Final workflow

Caller -> Exotel ExoPhone -> Voicebot Applet -> WSS /voice -> STT -> ConversationManager -> Scheme Matcher / FAQ / Ollama -> Hindi TTS -> 8 kHz PCM -> Exotel -> Caller

### Components
1. **Exotel Voicebot**: bidirectional WebSocket media.
2. **Vosk Hindi**: local streaming speech-to-text.
3. **ConversationManager**: existing profile, memory, scheme and Ollama logic.
4. **Piper Hindi**: local text-to-speech.
5. **Ollama llama3.2:3b**: Hindi response generation.

Exotel's current documentation specifies bidirectional Voicebot media as base64-encoded 16-bit linear PCM, mono, 8 kHz by default. Outbound bot audio is sent back as `media` messages. Exotel does not provide STT/TTS for the Voicebot stream, so those are handled locally here.

## Setup

Use the separate Python 3.13 environment you already created:

```powershell
C:\venvs\jansahayak\Scripts\python.exe -m pip install -r requirements.txt
C:\venvs\jansahayak\Scripts\python.exe scripts\download_voice_models.py
C:\venvs\jansahayak\Scripts\python.exe scripts\test_tts.py
```

The TTS test creates `audio\outgoing\test_hindi_8khz.wav`.

## Start

Terminal 1 — keep Ollama running (your existing Ollama service is enough).

Terminal 2:
```powershell
C:\venvs\jansahayak\Scripts\python.exe voice_server.py
```

Terminal 3:
```powershell
ngrok http 8000
```

Then use the current ngrok HTTPS hostname with `/voice` as the Exotel WSS endpoint:

`wss://YOUR-NGROK-HOST/voice`

## Exotel Voicebot settings

- URL: `wss://YOUR-NGROK-HOST/voice`
- Record: Off for the first prototype
- Encrypt DTMF: Off for the first prototype
- Next applet: optional; the Voicebot can end the flow when the WebSocket closes.

## Important

The free ngrok hostname can change between sessions. If it changes, update the Exotel Voicebot URL.

The current implementation is **turn-based**: caller speaks -> silence is detected -> STT -> AI -> TTS -> audio is played. It is not yet full-duplex barge-in. That can be added after the basic call path works.
