import logging
import requests
from pathlib import Path
from app.functions.utils.misc import get_lecture_number


def generate_chunk_tex(chunk_path: Path, output_path: Path, api_url: str):
    try:
        content = ""
        with open(chunk_path, "r", encoding="utf-8") as f:
            content = f.read()

        messages = [
            {
                "role": "user",
                "content": (
                    "Ты — строгий LaTeX-ассистент. "
                    "Твоя задача: строго переписать переданный транскрибированный текст лекции в LaTeX-оформлении. "
                    "Запрещено придумывать текст. Запрещено писать «ваш текст содержит...». Запрещено дублировать шаблоны. "
                    "Просто возьми исходный текст и структурируй его в LaTeX: добавляй \\section, \\subsection, \\itemize, \\begin{gather*}, $...$ где это уместно. "
                    "Не добавляй преамбулу, не пиши \\begin{document}, не объясняй текст. "
                    "Сохраняй ошибки, стиль и порядок слов лектора. "
                    "Если текст бессвязный — всё равно оформляй его дословно в LaTeX. "
                    "Не исправляй, не редактируй, не добавляй вступлений и заключений."
                    f"Вот чанк транскрипта лекции:\n\n{content}"
                )
            }
        ]

        payload = {
            "model": "qwen2-1.5b-instruct",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 2048,
            "stream": False
        }

        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        tex = response.json()["choices"][0]["message"]["content"]

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(tex)

        logging.info(f"LaTeX сгенерирован: {output_path}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при обращении к API: {str(e)}")
        raise

    except Exception as e:
        logging.error(f"Ошибка генерации LaTeX из чанка {chunk_path.name}: {str(e)}")
        raise


def convert_chunks_to_latex(video_path: Path, transcript_base_dir: Path, output_base_dir: Path, api_url: str):
    """
    Конвертирует транскрипты лекции в LaTeX, используя локальный LLM.
    :param video_path: исходное видео (для определения номера лекции)
    :param transcript_base_dir: директория с транскриптами
    :param output_base_dir: директория, куда сохраняются .tex
    :param api_url: URL OpenAI-совместимого API
    """
    lecture_num = get_lecture_number(video_path)
    transcript_dir = transcript_base_dir / f"lecture_{lecture_num}"
    output_dir = output_base_dir / f"lecture_{lecture_num}"

    transcript_paths = sorted(transcript_dir.glob("chunk_*.txt"))
    if not transcript_paths:
        raise FileNotFoundError(f"Нет транскриптов в {transcript_dir}")

    for chunk_path in transcript_paths:
        chunk_num = chunk_path.stem.split("_")[-1]
        output_path = output_dir / f"chunk_{chunk_num}.tex"
        if output_path.exists():
            logging.info(f"Пропущено (уже есть): {output_path.name}")
            continue
        generate_chunk_tex(chunk_path, output_path, api_url) 