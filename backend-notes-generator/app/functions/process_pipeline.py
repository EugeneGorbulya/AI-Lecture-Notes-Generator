from pathlib import Path
import logging
from app.functions.transcriber.splitter import split_video
from app.functions.transcriber.whisperer import transcribe_chunks
from app.functions.converter.tex_generator import convert_chunks_to_latex
from app.functions.tools.merger import merge_tex_chunks
from app.functions.utils.misc import get_lecture_number
from app.core.config import settings

OPENAI_API_URL = settings.OPENAI_API_URL


def process_video_to_tex(video_path: str, files_dir: str) -> str:
    logging.info(f"Старт обработки видео: {video_path}")
    video_path = Path(video_path)
    files_dir = Path(files_dir)

    chunks_dir = files_dir / "chunks"
    logging.info(f"Нарезка видео в: {chunks_dir}")
    try:
        split_video(video_path, chunks_dir)
        logging.info(f"Нарезка завершена. Чанки в: {chunks_dir}")
    except Exception as e:
        logging.error(f"Ошибка при нарезке видео: {e}")
        raise

    transcripts_dir = files_dir / "transcripts"
    logging.info(f"Транскрипция чанков в: {transcripts_dir}")
    try:
        transcribe_chunks(video_path, chunks_dir, transcripts_dir)
        logging.info(f"Транскрипция завершена.")
    except Exception as e:
        logging.error(f"Ошибка при транскрипции: {e}")
        raise

    tex_dir = files_dir / "tex"
    logging.info(f"Генерация LaTeX в: {tex_dir}")
    try:
        convert_chunks_to_latex(video_path, transcripts_dir, tex_dir, OPENAI_API_URL)
        logging.info(f"Генерация LaTeX завершена.")
    except Exception as e:
        logging.error(f"Ошибка при генерации LaTeX: {e}")
        raise

    lecture_num = get_lecture_number(video_path)
    logging.info(f"Объединение чанков в один .tex файл для лекции #{lecture_num}")
    try:
        merge_tex_chunks(lecture_num, tex_dir, cleanup=True)
    except Exception as e:
        logging.error(f"Ошибка при объединении .tex файлов: {e}")
        raise

    final_tex = tex_dir / f"lecture_{lecture_num}.tex"
    if not final_tex.exists():
        logging.error(f"Итоговый .tex файл не найден: {final_tex}")
        raise FileNotFoundError(f"Итоговый .tex файл не найден: {final_tex}")

    logging.info(f"Обработка завершена. Итоговый файл: {final_tex}")
    return str(final_tex)
