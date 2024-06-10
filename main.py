import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import click


import json
import time

from raspberry_pi import RaspberryPi

IPS = ["localhost"]
RFID_ID = json.load(open("rfids.json", encoding='utf-8'))

PIS: list[RaspberryPi] = [RaspberryPi(ip, host_password="admin", init_playlist=False) for ip in IPS]


READER = SimpleMFRC522()
is_playing = False

def check_video_completion() -> None:
    for pi in PIS:
        pi.update_status()
        if pi.status.time == pi.status.length:
                pi.stop()
                
def play(rfid: str):
    for pi in PIS:
        pi.play(RFID_ID, rfid)

    
def main():
    while True:
        try:
            id, text = READER.read()
            play(id)
            is_playing = True
        finally:
            GPIO.cleanup()
        
        
        if is_playing:
            check_video_completion()
            
        time.sleep(1)
    
        
    
if __name__ =="__main__":
    main()