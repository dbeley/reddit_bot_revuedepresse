# reddit_bot_revuedepresse

Reddit bot behind the /u/revuedepresse account.

## Installation of the virtualenv

```
pipenv install
```

## Requirements

= requests
- praw
- imgurpython
- imgur config (in the folder set in the systemd service file)
- praw.ini (in the folder set in the systemd service file)
- comment_inter.txt (in the folder set in the systemd service file)
- systemd files in ~/.config/systemd/user/
- [scrap_revuedepresse](https://github.com/dbeley/scrap_revuedepresse)

The systemd service needs some config files to be placed on the folder indicated in its WorkingDirectory directive for the service to work properly :

- praw.ini
- imgur config
- comment_inter.txt


## Usage

```
systemctl --user daemon-reload
systemctl --user enable --now reddit_bot_revuedepresse.timer
systemctl --user start reddit_bot_revuedepresse
```
