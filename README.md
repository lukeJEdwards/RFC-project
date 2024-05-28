# RFC project server

```
/status.json
/playlist.json

# ?command=pl_empty
# ?command=pl_loop
# ?command=fullscreen

# ?command=pl_play&id=<id>
# ?command=in_enqueue&input=<id>
# ?command=pl_delete&id=<id>

netstat -aon | findstr 8080
taskkill /f /pid 1234
scp <video> admin@192.168.1.149:Videos
ssh-keygen -R <ip>


sudo raspi-config

sudo apt-get update
sudo apt-get install vlc
sudo apt upgrade

sudo reboot
sudo apt autoremove
sudo apt clean

mkdir Videos

crontab -e
@reboot /home/admin/vlc-server.sh

chmod u+x vlc-server.sh

```
