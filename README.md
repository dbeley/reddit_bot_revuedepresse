# reddit_bot_revuedepresse

Reddit bot behind the /u/revuedepresse account.

## Requirements

- python-praw
- python-imgurpython
- imgur config (in the folder set in the systemd service file)
- praw.ini (in the folder set in the systemd service file)
- systemd files in ~/.config/systemd/user/
- [scrap_revuedepresse](https://github.com/dbeley/scrap_revuedepresse)

## Usage

```
systemctl --user daemon-reload
systemctl --user enable --now reddit_bot_revuedepresse.timer
systemctl --user start reddit_bot_revuedepresse
```
