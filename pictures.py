from pathlib import Path
from typing import Optional
from uuid import uuid4

import requests


def download_picture(url: Optional[str], pictures_dir: str):
    Path(pictures_dir).mkdir(exist_ok=True)
    res = requests.get(url)
    filename = Path(pictures_dir) / f"{uuid4()}.jpg"
    with open(filename, "wb") as fp:
        fp.write(res.content)
    return str(filename)
