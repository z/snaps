# Screenshot Notification Action Program S

SNAPS uses the notification system to prompt users for an action post-screenshot. 

When the bound hotkey that initiates the script is pressed, `scrot` is
executed is selection mode. After selecting part of the screen, a 
notification appears with buttons asking what action to execute next.

Default options include:

* Upload (uses scp configured in the config.ini
* Open with GIMP
* Cancel

#### Configuration

```
cp example.config.ini config.ini
```