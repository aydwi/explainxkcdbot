# A Reddit bot that posts explanation of xkcd comic strips posted in comments
# The explanation is extracted from http://explainxkcd.com
# Created by Ayush Dwivedi (/u/kindw)
# License: MIT License

from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = '/home/ayush/Projects/explainxkcdbot/commented.txt'
# Location of file where id's of already visited comments are maintained

header = '**Explanation of this xkcd:**\n'
footer = '\n*---This explanation was extracted from [explainxkcd](http://www.explainxkcd.com) | Bot created by u/kindw | [Source code](https://github.com/aydwi/explainxkcdbot)*'
# Text to be posted along with comic description


def authenticate():
    
    print('Authenticating...\n')
    reddit = praw.Reddit('explainbot', user_agent = 'web:xkcd-explain-bot:v0.1 (by /u/kindw)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def fetch_explanation(xkcd_id):

    # http://www.explainxkcd.com/wiki/api.php
    params = {
        'action': 'parse',
        'page': xkcd_id,
        # So we don't need to find out the XKCD title and somehow parse that
        'redirects': 'true',
        'prop': 'text',
        'format': 'json',
        # Only the transcript bit, not the discussion and other stuff we don't want
        'section': '1'
    }

    r = requests.get('http://www.explainxkcd.com/wiki/api.php/', params=params).json()

    # Invalid xkcd id or another error.
    # just raise an exception so the call below doesn't have to be modified
    if 'error' in r:
        raise Exception

    soup = BeautifulSoup(r['parse']['text']['*'], 'html.parser')

    # Remove the "Explanation" h2
    soup.find('h2').decompose()

    # Remove all html
    explanation = soup.get_text(separator="\n")

    # Remove single whitespace (that isn't preceeded or succeeded by a \n),
    # which will only be from inline bits inside the <p> tags
    # (Isn't really necessary, but produces an ugly output otherwise,
    # but still looks good after Markdown does its magic)
    return re.sub('(?<!\n)(\n)(?!\n)', '', explanation).strip()


def run_explainbot(reddit):
    
    print("Getting 250 comments...\n")
    
    for comment in reddit.subreddit('test').comments(limit = 250):
        match = re.findall("[a-z]*[A-Z]*[0-9]*https://www.xkcd.com/[0-9]+", comment.body)
        if match:
            print('Link found in comment with comment ID: ' + comment.id)
            xkcd_url = match[0]
            print('Link: ' + xkcd_url)

            url_obj = urlparse(xkcd_url)
            xkcd_id = int((url_obj.path.strip("/")))
            
            file_obj_r = open(path,'r')
                        
            try:
                explanation = fetch_explanation(xkcd_id)
            except:
                print('Exception!!! Possibly incorrect xkcd URL...\n')
                # Typical cause for this will be a URL for an xkcd that does not exist (Example: https://www.xkcd.com/772524318/)
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    comment.reply(header + explanation + footer)
                    
                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')
            
            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)


def main():
    reddit = authenticate()
    while True:
        run_explainbot(reddit)


if __name__ == '__main__':
    main()
