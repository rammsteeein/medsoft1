from celery import Celery
import whisper
import os

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

model = whisper.load_model("medium")


@celery_app.task
def transcribe_audio_task(audio_path: str):
    try:
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)

        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)

        os.remove(audio_path)

        return {
            "detected_language": detected_language,
            "transcription": result.text
        }
    except Exception as e:
        return {"error": str(e)}