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
    os.chdir(directory)
    logger.debug(os.getcwd())
    config_album = {
            'privacy': "public"
            }

    album = client.create_album(config_album)

    pathlist = Path(directory).glob('*.jpg')
    for file in sorted(pathlist):
        title_file = Path(file).stem.split('_', 1)[-1].replace('_', ' ')
        config_image = {
                'album': album['deletehash'],
                'privacy': "public",
                'title': title_file
                }
        logger.debug(f"Upload image {file}, with title {title_file}")
        client.upload_from_path(str(file), config=config_image)
        time.sleep(8)

    final_url = f"https://imgur.com/a/{album['id']}"
    logger.debug(final_url)

    return(final_url)


def main():
    args = parse_args()
    test = args.test
    folder = args.folder
    post_to_reddit = args.post_to_reddit
    international = args.international
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    jour = datetime.datetime.now().strftime("%A %d %B %Y")
    config = configparser.RawConfigParser()
    config.read('config_imgur')
    client_id = config['imgur']['client_id']
    client_secret = config['imgur']['client_secret']
    client = ImgurClient(client_id, client_secret)

    if test:
        reddit = redditconnect('revuedepresse_test')
    else:
        reddit = redditconnect('revuedepresse')

    with open('comment_inter.txt', 'r') as myfile:
        comment_inter = myfile.read()

    if folder:
        directory_imgur = folder
    else:
        if international:
            directory_imgur = f"Images/{auj}_international/"
        else:
            directory_imgur = f"Images/{auj}/"
    logger.debug(f"Upload à imgur du dossier {directory_imgur}")

    if not os.path.isdir(directory_imgur):
        logger.error("The folder containing the images doesn't exist or has not been created by the scrap_revuedepresse script.")
        exit()

    try:
        url = imgur_folder_upload(directory_imgur, client)
    except Exception as e:
        logger.error(str(e))
        exit()

    if post_to_reddit:
        if international:
            logger.debug("Sending comment (international version)")
            rdp = reddit.user.me()
            for post in rdp.submissions.new():
                post.reply(eval(comment_inter))
                break
        else:
            logger.debug("Sending post")
            if test:
                post = reddit.subreddit("test").submit(f"Revue de presse du {jour}", url=url)
            else:
                post = reddit.subreddit("france").submit(f"Revue de presse du {jour}", url=url)
                post.flair.select("48645bbe-1363-11e4-b184-12313b01142d")
    else:
        logger.debug("No-reddit mode activated. Nothing will be posted.")

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Reddit bot')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--folder', help="Folder containing the images to export", type=str)
    parser.add_argument('-t', '--test', help="Switch from the revuedepresse to the revuedepresse_test user", dest='test', action='store_true')
    parser.add_argument('-n', '--no-reddit', help="Alternative to test, without posting to reddit", dest='post_to_reddit', action='store_false')
    parser.add_argument('-i', '--international', help="Add a comment containing the international version on the last post of the user", dest='international', action='store_true')
    parser.set_defaults(test=False, international=False, post_to_reddit=True)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
