from __future__ import annotations
from dataclasses import dataclass
from dill import dumps, loads

from enums import ORIENTATION, VIDEO_EVENT, EVENT_TYPE
    
    
@dataclass
class videoInfo:
    fileName: str
    length: int
    currentTime: int
    orientation: ORIENTATION
    
    
@dataclass
class piInfo:
    ip: str
    hostName: str
    isPlaying: bool
    currentlyPlaying: videoInfo
    
@dataclass
class readerInfo:
    id: str
    prevouisTag: str
    currentTag: str
    timeElapse: float
    
    
@dataclass
class event:
    type: EVENT_TYPE
    
    def serialize(self) -> bytes:
        return dumps(self)
    
    @classmethod
    def deserialize(cls, data: bytes) -> event:
        return cls(loads(data))
    
@dataclass
class videoEvent(event):
    videoState: VIDEO_EVENT
    data: piInfo
    
@dataclass
class readerEvent(event):
    data: readerInfo
        