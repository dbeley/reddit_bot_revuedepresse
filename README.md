# reddit_bot_revuedepresse

## Requirements

- python-praw
- python-imgurpython
- imgur config
- praw.ini
- systemd files in ~/.config/systemd/user/
- [scrap_revuedepresse](https://github.com/dbeley/scrap_revuedepresse)

## Usage

```
systemctl --user daemon-reload
systemctl --user enable --now reddit_bot_revuedepresse.timer
systemctl --user start reddit_bot_revuedepresse
```
