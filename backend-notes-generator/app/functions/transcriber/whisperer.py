import subprocess
import logging
import whisper
from pathlib import Path
from app.functions.config import WHISPER_MODEL
from app.functions.utils.misc import get_lecture_number


def extract_audio(chunk: Path, wav_path: Path):
    command = [
        "ffmpeg", "-loglevel", "error",
        "-y", "-i", str(chunk),
        "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le", str(wav_path)
    ]
    subprocess.run(command, check=True)


def transcribe_chunk(chunk: Path, transcript_path: Path, model):
    wav_path = chunk.with_suffix(".wav")
    extract_audio(chunk, wav_path)
    result = model.transcribe(str(wav_path), language="ru")
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())
    logging.info(f"Сохранён транскрипт: {transcript_path.name}")


def transcribe_chunks(video_path: Path, chunk_base_dir: Path, transcript_base_dir: Path):
    """
    Транскрибирует все чанки, связанные с заданным видео.
    :param video_path: путь до исходного видео
    :param chunk_base_dir: директория, где хранятся чанки
    :param transcript_base_dir: директория для сохранения транскриптов
    """
    lecture_num = get_lecture_number(video_path)
    chunk_dir = chunk_base_dir / f"lecture_{lecture_num}"
    transcript_dir = transcript_base_dir / f"lecture_{lecture_num}"

    chunks = sorted(chunk_dir.glob("chunk_*.mp4"))
    if not chunks:
        raise FileNotFoundError(f"Нет чанков для лекции {lecture_num}")

    model = whisper.load_model(WHISPER_MODEL)
    for chunk in chunks:
        name = chunk.stem
        transcript_path = transcript_dir / f"{name}.txt"
        if transcript_path.exists():
            logging.info(f"{name} уже транскрибирован.")
            continue
        transcribe_chunk(chunk, transcript_path, model) 