#!/usr/bin/env python3

# A Reddit bot that posts explanation of xkcd comic strips posted in the
# comments. The explanation is extracted from http://explainxkcd.com

import os
import praw
import time
import re
import requests
import bs4

from bs4 import BeautifulSoup
from urllib.parse import urlparse


# Path of file where IDs of already visited comments are maintained
commented_path = "commented.txt"

# Text to be posted along with comic description
header = "**Explanation of this xkcd:**\n"
footer = (
    "\n*---This explanation was extracted from"
    " [explainxkcd](http://www.explainxkcd.com)"
    " | [Source](https://github.com/aydwi/explainxkcdbot)*"
)


def authenticate():
    print("Authenticating...\n")
    reddit = praw.Reddit("explainbot", user_agent="web:xkcd-explain-bot:v0.1")
    print("Authenticated as {}\n".format(reddit.user.me()))
    return reddit


def fetchdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    tag = soup.find("p")
    data = ""
    while True:
        if isinstance(tag, bs4.element.Tag):
            if tag.name == "h2":
                break
            if tag.name == "h3":
                tag = tag.nextSibling
            else:
                data = data + "\n" + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
    return data


def run_explainbot(reddit):
    print("Getting 250 comments...\n")
    for comment in reddit.subreddit("test").comments(limit=250):
        match = re.findall("https://www.xkcd.com/[0-9]+", comment.body)
        if match:
            print("Link found in comment with comment ID: " + comment.id)
            xkcd_url = match[0]
            print("Link: " + xkcd_url)

            url_obj = urlparse(xkcd_url)
            xkcd_id = int((url_obj.path.strip("/")))
            target_url = "http://www.explainxkcd.com/wiki/index.php/" + str(
                xkcd_id
            )

            if not os.path.exists(commented_path):
                open(commented_path, "w").close()
            file_obj_r = open(commented_path, "r")

            try:
                explanation = fetchdata(target_url)
            except Exception as e:
                print("An exception occured - " + str(e) + "\n")
                # Typical cause for this can be a URL for an xkcd that
                # does not exist.
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print("Link is unique...posting explanation\n")
                    comment.reply(header + explanation + footer)

                    file_obj_r.close()

                    file_obj_w = open(commented_path, "a+")
                    file_obj_w.write(comment.id + "\n")
                    file_obj_w.close()
                else:
                    print("Already visited link...no reply needed\n")
            time.sleep(10)

    print("Waiting 60 seconds...\n")
    time.sleep(60)


def main():
    reddit = authenticate()
    while True:
        run_explainbot(reddit)


if __name__ == "__main__":
    main()
