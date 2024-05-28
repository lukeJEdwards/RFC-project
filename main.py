# from PiicoDev_RFID import PiicoDev_RFID
# from PiicoDev_Unified import sleep_ms

import json
import time

from raspberry_pi import RaspberryPi

IPS = ["192.168.1.149", "192.168.1.205"]
RFID_ID = json.load(open("rfids.json", encoding='utf-8'))

PIS: list[RaspberryPi] = [RaspberryPi(ip, host_password="admin", init_playlist=False) for ip in IPS]
# RFID_READERS = [PiicoDev_RFID(asw=[0, 0]), PiicoDev_RFID(asw=[0, 1]), PiicoDev_RFID(asw=[1, 0]), PiicoDev_RFID(asw=[1, 1])]


def check_video_completion() -> None:
    for pi in PIS:
        pi.update_status()
        if pi.status.time == pi.status.length:
                pi.stop()
                
def play(rfid: str):
    for pi in PIS:
        pi.play(RFID_ID, rfid)

    
def main():
    play("r3")
    while True:
        check_video_completion()
        time.sleep(1)
    
        
    
if __name__ =="__main__":
    main()