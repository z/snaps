# Screenshot Notification Action Program S

snaps uses the notification system to prompt users for an action post-screenshot. 

When the bound hotkey that initiates the script is pressed, `scrot` is
executed in selection mode. After selecting part of the screen, a 
notification appears with buttons asking what action to execute next.

Default actions include:

* Upload (uses scp configured in the config.ini)
* Open with GIMP
* Cancel

#### Requirements

```
sudo apt-get install python3-gobject scrot
```

#### Configuration

```
cp example.config.ini config.ini
```

The configuration contents should appear similar to below:

```
[default]

local_screenshot_path = ~/screenshots/clippings/
remote_screenshot_path = ~/web.example.com/html/screenshots/
remote_user = user
remote_server = ssh.example.com
remote_server_url = http://example.com/screenshots/
```

In order to scp without a password, you'll need to copy your ssh key over
 to your server.

```
ssh-copy-id user@server
```

#### Usage

```
python3 snaps.py
```