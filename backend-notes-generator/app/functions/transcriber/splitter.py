import subprocess
import logging
from pathlib import Path
from app.functions.config import CHUNK_DURATION_MIN
from app.functions.utils.misc import get_lecture_number


def split_video(video_path: Path, output_base_dir: Path, force=False) -> Path:
    """
    Разрезает видео на чанки и сохраняет их в output_base_dir/lecture_{num}/chunk_XXX.mp4
    :param video_path: путь до видеофайла
    :param output_base_dir: базовая директория для чанков (например: /lectex_output/chunks)
    :param force: если True — удаляет старые чанки и режет заново
    :return: путь до директории с чанками
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Видео не найдено: {video_path}")

    lecture_num = get_lecture_number(video_path)
    output_dir = output_base_dir / f"lecture_{lecture_num}"
    output_dir.mkdir(parents=True, exist_ok=True)

    existing_chunks = list(output_dir.glob("chunk_*.mp4"))
    if existing_chunks and not force:
        logging.info(f"Чанки уже существуют в {output_dir}, разрезка пропущена.")
        return output_dir

    if force and existing_chunks:
        for f in existing_chunks:
            f.unlink()
        logging.info(f"Удалены старые чанки в {output_dir}")

    command = [
        "ffmpeg", "-i", str(video_path),
        "-c", "copy", "-map", "0",
        "-segment_time", str(CHUNK_DURATION_MIN * 60),
        "-f", "segment", "-reset_timestamps", "1",
        str(output_dir / "chunk_%03d.mp4")
    ]

    logging.info(f"Разрезка видео {video_path.name} на чанки...")
    try:
        subprocess.run(command, check=True)
        logging.info(f"Разрезка завершена: {output_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка разрезки: {e}")
        raise

    return output_dir 