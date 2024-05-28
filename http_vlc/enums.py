from __future__ import annotations
from enum import StrEnum, auto

class VLC_RESOURCE(StrEnum):
    playlist = auto()
    status = auto()
    
class VLC_PARAM_CMD(StrEnum):
    in_enqueue = auto()    
    pl_play = auto() 
    pl_pause = auto() 
    pl_delete = auto() 
    
    def get_param(cmd: VLC_PARAM_CMD) -> str:
        match cmd:
            case VLC_PARAM_CMD.in_enqueue:
                return "input="
            case VLC_PARAM_CMD.pl_play | VLC_PARAM_CMD.pl_pause | VLC_PARAM_CMD.pl_delete:
                return "id="
            case _:
                return ""

class VLC_CMD(StrEnum):
    pl_forceresume = auto() 
    pl_forcepause = auto() 
    pl_stop = auto() 
    pl_next = auto() 
    pl_previous = auto() 
    pl_empty = auto() 
    pl_loop = auto() 
    pl_repeat = auto() 
    fullscreen = auto()
    
    
class PLAYLIST_NODE_TYPE(StrEnum):
    node = auto()
    leaf = auto()
    
class PLAYLIST_RO_TYPE(StrEnum):
    ro = auto()
    rw = auto()