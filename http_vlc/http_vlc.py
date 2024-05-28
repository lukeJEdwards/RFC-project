"""
httpVLC class
Usage: control a HTTP server vlc starts 
Based on https://github.com/MatejMecka/python-vlc-http/blob/master/python_vlc_http/vlc.py
"""

from dataclasses import dataclass, field
from typing import Any

from .exceptions import MissingHost, InvalidCredentials, RequestFailed
from .enums import VLC_RESOURCE, VLC_PARAM_CMD, VLC_CMD
from .mappings import VLCStatus, PlaylistTreeNode

from httpx import Response, Client
import httpx
    

@dataclass
class HttpVLC:
    host:str = field(default=None)
    port: str = field(default="8080")
    username: str = field(default="")
    password: str = field(default="")
    
    client: Client = field(default_factory=Client)
    
    
    def __post_init__(self) -> None:
        if not self.host or self.host is None:
            raise MissingHost("Host is empty! Input host to proceed")
        
    @property
    def BASE_URL(self) -> str:
        return f'http://{self.username}:{self.password}@{self.host}:{self.port}/requests'
        
    def _status_code(self, request: Response):
        
        match request.status_code:
            case 200:
                return True
            case 401:
                raise InvalidCredentials("Unathorized! The provided username or password were incorrect")
            case _:
                raise RequestFailed(f"Query failed, response code: {request.status_code} Full message: {request.text}")
        
        
    def _fetch_api(self, resource: VLC_RESOURCE, cmd="") -> dict[str, Any]:
        try:
            response = self.client.get(f"{self.BASE_URL}/{resource}.json{cmd}")
            self._status_code(response)
            return response.json()
        except (httpx._exceptions.ConnectError, httpx._exceptions.TimeoutException) as error:
            raise RequestFailed(f"The VLC Server is unreachable. Error code: {error}")
        
    def _is_closed(self) -> None:
        if self.client.is_closed:
            raise httpx._exceptions.CloseError("Client is closed")
    
    def get_playlist(self, name="Playlist") -> PlaylistTreeNode | None:
        self._is_closed()
        return PlaylistTreeNode(**self._fetch_api(VLC_RESOURCE.playlist)).get_playlist(name=name)
        
    
    def get_status(self) -> dict[str, Any]:
        self._is_closed()
        return VLCStatus(**self._fetch_api(VLC_RESOURCE.status))
    
    def give_command(self, cmd:VLC_PARAM_CMD | VLC_CMD, param="") -> dict[str, Any]:
        self._is_closed()
        if param:
            return self._fetch_api(VLC_RESOURCE.status, f'?command={cmd}&{VLC_PARAM_CMD.get_param(cmd)}{param}')
        return self._fetch_api(VLC_RESOURCE.status, f'?command={cmd}')
    
    def close(self) -> None:
        self.client.close()