# reddit_bot_revuedepresse

Reddit bot behind the /u/revuedepresse account.

## Installation of the virtualenv (recommended)

```
pipenv install
```

## Requirements

- requests
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

## Help

```
python reddit_bot_revuedepresse.py -h
```

```
usage: reddit_bot_revuedepresse.py [-h] [--debug] [-f FOLDER] [-t] [-n] [-i]

Reddit bot

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -f FOLDER, --folder FOLDER
                        Folder containing the images to export
  -t, --test            Switch from the revuedepresse to the
                        revuedepresse_test user
  -n, --no-reddit       Alternative to test, without posting to reddit
  -i, --international   Add a comment containing the international version on
                        the last post of the user
```
