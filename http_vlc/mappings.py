from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from .enums import PLAYLIST_NODE_TYPE, PLAYLIST_RO_TYPE


@dataclass
class PlaylistTreeBase:
    name: str
    id: int
    ro: PLAYLIST_RO_TYPE
    type: PLAYLIST_NODE_TYPE
    
@dataclass
class PlaylistTreeLeaf(PlaylistTreeBase):
    uri: str
    duration: int
    current: str = field(default="")
    
@dataclass
class PlaylistTreeNode(PlaylistTreeBase):
    children: list[PlaylistTreeNode | PlaylistTreeLeaf] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        self.children = list(map(lambda child: self.make_tree(child), self.children))

    def make_tree(self, obj: dict[str, Any]) -> PlaylistTreeNode | PlaylistTreeLeaf:
        return PlaylistTreeNode(**obj) if obj["type"] == PLAYLIST_NODE_TYPE.node else PlaylistTreeLeaf(**obj)
    
    def get_playlist(self, name:str = "Playlist") -> PlaylistTreeNode | None:
        pl =  [playlist for playlist in self.children if playlist.name == name]
        if len(pl) == 0:
            return None
        return pl[0]
        
    
@dataclass
class VideoInfomation:
    chapter: int = field(default=None)
    chapters: list[int] = field(default=None)
    category: dict[str, dict[str, str]] = field(default=None)
    titles:list[int] = field(default=None)
    title:int = field(default=None)
    
@dataclass
class VideoStats:
    sentpackets: int = field(default=None)
    demuxreadpackets: int = field(default=None)
    decodedaudio: int = field(default=None)
    averageinputbitrate: int = field(default=None)
    lostpictures: int = field(default=None)
    averagedemuxbitrate: int = field(default=None)
    readbytes: int = field(default=None)
    sendbitrate: int = field(default=None)
    displayedpictures: int = field(default=None)
    readpackets: int = field(default=None)
    demuxcorrupted: int = field(default=None)
    decodedvideo: int = field(default=None)
    lostabuffers: int = field(default=None)
    playedabuffers: int = field(default=None)
    demuxbitrate: float = field(default=None)
    demuxreadbytes: int = field(default=None)
    inputbitrate: float = field(default=None)
    demuxdiscontinuity: int = field(default=None)
    sentbytes: int = field(default=None)
    
@dataclass
class VLCStatus:
    loop: bool
    audiodelay: int
    volume: int
    seek_sec: int
    state: bool
    apiversion: int
    subtitledelay: int
    random: bool
    time: int
    repeat: bool
    version: str
    currentplid: int
    rate:int
    length: int
    fullscreen: bool
    position: int
    aspectratio: str = field(default=None)
    audiofilters: dict[str, str] = field(default_factory=dict)
    information: VideoInfomation = field(default_factory=VideoInfomation)
    stats: VideoStats = field(default_factory=VideoStats)
    equalizer: list = field(default_factory=list)
    videoeffects: dict[str, int] = field(default_factory=dict)
    