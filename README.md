# 🇯🇵 Japanese Speaking Practice AI

A simple local AI project to help you **practice speaking Japanese**.  
It can generate sentences, convert your speech to text, check your grammar, and score your pronunciation.

---

## Features
- 🎙 Speech-to-text using **Whisper**
- ✍️ Random Japanese text generation (basic, intermediate, advanced)
- 🧩 Grammar correction - TBD
- 🗣 Pronunciation similarity scoring
- 🔤 Romaji and English translation
- ⚡ Built with **FastAPI** backend

---

## requirements.txt

```txt
fastapi
uvicorn
transformers
torch
sentencepiece
pykakasi
googletrans==4.0.0-rc1
jiwer
openai-whisper
numpy
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Example Usage

### Generate a practice sentence
```bash
GET /generate_text?level=basic
```

**Response**
```json
{
  "level": "basic",
  "practice_text": "私は毎朝パンを食べます。",
  "romaji": "watashi wa mai asa pan o tabemasu 。",
  "translation": "I eat bread every morning."
}
```

---

## Notes
- Works fully **offline** using local models.
- You can replace models with larger or fine-tuned ones later.
- Translation is optional (remove googletrans if offline-only).
