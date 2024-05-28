import paramiko

from dataclasses import dataclass, field, InitVar

from http_vlc import HttpVLC, PlaylistTreeNode, VLCStatus
from http_vlc.enums import VLC_PARAM_CMD, VLC_CMD


@dataclass
class RaspberryPi:
    IP: str
    host_username:str = field(default="")
    host_password:str = field(default="")
    
    SSH_username: str = field(default="admin")
    SSH_password: str = field(default="admin")
    
    videos: list[str] = field(default=None)
    
    vlc_client: HttpVLC = field(default=None)
    playlist: PlaylistTreeNode = field(default=None)
    status: VLCStatus = field(default=None)
    
    init_playlist: InitVar[bool] = field(default=True)
    
    def __post_init__(self, init_playlist: bool) -> None:
        self.vlc_client = HttpVLC(host=self.IP, username=self.host_username, password=self.host_password)
        
        self.videos = self._get_pi_videos()
        
        if init_playlist:
            self._setup_playlist()
        
        self.playlist = self.vlc_client.get_playlist()
        self.status = self.vlc_client.get_status()
        

    def _get_pi_videos(self) -> list[str]:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if self.SSH_username and self.SSH_password:
            client.connect(self.IP, username=self.SSH_username, password=self.SSH_password)
        else:
            client.connect(self.IP)
            
        stdin, stdout, stderr = client.exec_command('ls Videos')
        files = [line.strip('\n') for line in stdout]
        client.close()
        return files
    
    def _setup_playlist(self) -> None:
        for video in self.videos:
            self.vlc_client.give_command(VLC_PARAM_CMD.in_enqueue, f'Videos/{video}')
        
           
            
    def update_status(self) -> None:
        self.status = self.vlc_client.get_status()
            
    def play(self, RFID: dict[str, str], rfid:str) -> None:
        video_name = RFID[rfid]
        video = list(filter(lambda vid: vid.name == video_name, self.playlist.children))[0]
        self.vlc_client.give_command(VLC_PARAM_CMD.pl_play, str(video.id))
        
    def stop(self) -> None:
        self.vlc_client.give_command(VLC_CMD.pl_stop)