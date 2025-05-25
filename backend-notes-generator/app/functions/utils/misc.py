import re
from pathlib import Path

def get_lecture_number(path: Path) -> int:
    """
    Извлекает номер лекции из имени файла или пути.
    """
    match = re.search(r'(\d+)', str(path))
    if match:
        return int(match.group(1))
    raise ValueError(f"Не удалось определить номер лекции из {path}") 