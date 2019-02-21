import datetime
import time
import argparse
import praw
import os
import logging
import locale
import errno
import configparser
from imgurpython import ImgurClient
from pathlib import Path

logger = logging.getLogger()
temps_debut = time.time()


def redditconnect(bot):
    user_agent = "python:bot"

    reddit = praw.Reddit(bot, user_agent=user_agent)
    return reddit


def imgur_folder_upload(directory, client):
    logger.debug(os.getcwd())
    config_album = {
            'privacy': "public"
            }

    album = client.create_album(config_album)

    config_image = {
            'album': album['deletehash'],
            'privacy': "public"
            }
    logger.debug(os.getcwd())
    pathlist = Path(directory).glob('*.jpg')
    for file in sorted(pathlist):
        logger.debug(f"Upload image {file}")
        client.upload_from_path(str(file), config=config_image)

    final_url = f"https://imgur.com/a/{album['id']}"
    logger.debug(final_url)

    return(final_url)


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    jour = datetime.datetime.now().strftime("%A %d %B %Y")
    config = configparser.RawConfigParser()
    config.read('config_imgur')
    client_id = config['imgur']['client_id']
    client_secret = config['imgur']['client_secret']
    logger.debug("Connexion à imgur")
    client = ImgurClient(client_id, client_secret)

    logger.debug("Connexion à reddit")
    reddit = redditconnect('revuedepresse')

    directory = "Images"
    try:
        os.makedirs(os.path.expanduser(directory))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    os.chdir(directory)

    logger.debug("Scrapping")
    os.system("scrap_revuedepresse_simple")

    directory_imgur = auj + "/"

    logger.debug(f"Upload à imgur du dossier {directory_imgur}")
    url = imgur_folder_upload(directory_imgur, client)

    logger.debug("Envoi du message")
    reddit.subreddit("test").submit(f"Revue de presse du {jour}", url=url)

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Reddit bot')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
