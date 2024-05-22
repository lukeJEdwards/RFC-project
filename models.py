from dataclasses import dataclass, field


@dataclass
class video:
    name:str
    id:str
    duration:int


@dataclass
class statusResponse:
    fullscreen:int = field(default=None)
    currentplid:int = field(default=None)
    time:int = field(default=None)
    state:str = field(default=None)
    loop: bool = field(default=None)
    position:int = field(default=None)
    repeat:bool = field(default=None)
    