from pathlib import Path

from os import listdir
from os.path import isfile, join

from dotenv import dotenv_values

import httpx


CONFIG = dotenv_values(".env")
BASE_URL = f"http://:{CONFIG["PASSWORD"]}@127.0.0.1:8080/requests"

DIR = "videos"

def main():
    file_path = f'{Path.cwd()}\\{DIR}'
    files = [join(file_path, f) for f in listdir(file_path) if isfile(join(file_path, f))]
    
    urls = [f'{BASE_URL}/playlist.json?command=in_enqueue&input={file}' for file in files]
    
    for url in urls:
        httpx.get(url)

if __name__ == "__main__":
    main()