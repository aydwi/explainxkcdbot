# An independent program to fetch and display explanation of
# an xkcd comic by providing its serial number
# The explanation is extracted from http://explainxkcd.com
# License: MIT License


import requests
import bs4

from bs4 import BeautifulSoup

xkcd_id = 1024
# Replace xkcd_id with the serial number of xkcd you want the
# explanation for

url = 'http://www.explainxkcd.com/wiki/index.php/' + str(xkcd_id)

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')


def main():
    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if (tag.name == 'h2'):
                break
            if (tag.name == 'h3'):
                tag = tag.nextSibling
                # This skips the contents of the 'h3' tag, which
                # are irrelevant to the explanation
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
    print (data)


if __name__ == '__main__':
    main()
