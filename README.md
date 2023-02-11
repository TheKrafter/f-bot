# f-bot
anonymously swear at people, with optional logging for moderation purposes.


licensed under BSD 3 clause.


pull requests open, i follow the [unix philosopy](https://en.wikipedia.org/wiki/Unix_philosophy#Origin)

[discord](https://discord.gg/jve2cSnFZD)

### Usage
#### Install/run
Basic steps for unix-likes:
```bash
git clone https://github.com/TheKrafter/f-bot
cd f-bot/
cp example.config.yml config.yml
nano config.yml # put ur bot token where it says
pip install -U nextcord logging42 pyyaml
python3 bot.py
```
#### SystemD Service
Set up a (safe) way to autostart on systemd systems
```bash
sudo loginctl enable-linger $USER
nano /home/$USER/.config/systemd/user/f-bot.service
```
Paste in to the file you just editied:
```systemd
[Unit]
Description=f-bot discord bot

[Service]
ExecStart=/usr/bin/env python3 /home/tiramisu/f-bot/bot.py
WorkingDirectory=/home/tiramisu/f-bot/

[Install]
WantedBy=default.target
```
`Ctrl`+`o`, `Enter`, `Ctrl`+`x` to exit nano
```bash
systemctl --user daemon-reload
systemctl --user enable f-bot.service
```
