from typing import Any
from dotenv import dotenv_values

from models import statusResponse, video

import json
import httpx

CONFIG = dotenv_values(".env")
BASE_URL = f"http://:{CONFIG["PASSWORD"]}@127.0.0.1:8080/requests"

RFID_ID = json.load(open("rfids.json", encoding='utf-8'))

playlist = {}
status = statusResponse()


def update_status(response: dict[str, any]) -> None:
    for key in status.__dict__.keys():
        setattr(status, key, response[key])


def get_playlist() -> dict[str, video]:
    pl: dict[str, video] = {}
    
    response = httpx.get(f'{BASE_URL}/playlist.json').json()
    
    for v in response["children"][0]["children"]:
        new_video = video(name=v["name"], id=v["id"], duration=v["duration"])
        rfid = RFID_ID[new_video.name]
        pl[rfid] = new_video
        
    return pl

def get_status() -> statusResponse:
    response: dict[str, Any] = httpx.get(f'{BASE_URL}/status.json').json()
    return update_status(response)

def play_video(id:str) -> statusResponse:
    response = httpx.get(f'{BASE_URL}/status.json?command=pl_play&id={id}')
    return update_status(response.json())

def stop_video() -> statusResponse:
    response = httpx.get(f'{BASE_URL}/status.json?command=pl_stop')
    return update_status(response.json())
    
def main():
    playlist = get_playlist()
    status = get_status()
    
    while True:
        pass
        
    
    
if __name__ =="__main__":
    main()


'''
video stats
/status.json

playlist stats
/playlist.json

empty playlist
?command=pl_empty

loop video
?command=pl_loop

fullscreen
?command=fullscreen

play video
?command=pl_play&id=<id>

netstat -aon | findstr 8080
taskkill /f /pid 1234
'''