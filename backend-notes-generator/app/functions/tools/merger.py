import logging
from pathlib import Path

def merge_tex_chunks(lecture_num: int, tex_dir: Path, cleanup: bool = True):
    lecture_dir = tex_dir / f"lecture_{lecture_num}"
    output_file = tex_dir / f"lecture_{lecture_num}.tex"
    
    chunk_files = sorted(lecture_dir.glob("chunk_*.tex"))

    if not chunk_files:
        logging.warning(f"Нет .tex файлов в {lecture_dir}")
        return

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as out:
        for chunk_path in chunk_files:
            with open(chunk_path, "r", encoding="utf-8") as f:
                out.write(f"% --- {chunk_path.name} ---\n")
                out.write(f.read())
                out.write("\n")

    logging.info(f"Файл лекции собран: {output_file}")

    if cleanup:
        for f in chunk_files:
            f.unlink()
        logging.info(f"Удалены чанки .tex из {lecture_dir}") 