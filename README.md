# explainxkcdbot
A Reddit bot that posts explanation of the [xkcd](https://www.xkcd.com/) links posted in the comments. The explanation is extracted from the [explain xkcd wiki](http://explainxkcd.com).

### Requirements-
1. Python 3
2. `pip` for Python 3 (recommended, but not necessary)
   * For installation see [here](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers) and [here](https://pip.pypa.io/en/stable/installing/).
2. PRAW
   * Install by running `pip3 install praw`.
3. Python Requests
   * Install by running `pip3 install requests`.
4. Beautiful Soup 4
   * Install by running `pip3 install beautifulsoup4`.
   
Using [`virtualenv`](https://github.com/pypa/virtualenv) to create a “virtual” isolated Python installation and install packages into that installation is recommended.


### Obtaining Reddit API access credentials-
1. Create a [Reddit](https://www.reddit.com/) account, and while logged in, navigate to preferences > apps
2. Click on the **are you a developer? create an app...** button
3. Fill in the details-
    * name: Name of your bot/script
    * Select the option 'script'
    * decription: Put in a description of your bot/script
    * redirect uri: `http://localhost:8080`
4. Click **create app**
5. You will be given a `client_id` and a `client_secret`. Keep them confidential.

### How to run it-
1. Clone this repository and navigate to its directory.
2. Create a file named *praw.ini* with its contents as:
    ```
    [explainbot]
    username: reddit username
    password: reddit password
    client_id: client_id that you got
    client_secret: client_secret that you got
    ```
3. Create an empty text file named *commented.txt* inside the project directory.
4. In *explainxkcdbot.py*, replace the value of `path` with the location of *commented.txt*.
5. Run `python3 explainxkcdbot.py` to run the bot.

### Additional notes-
1. It is possible to use other file types (even plain text) to store the authentication credentials, but creating and using *praw.ini* is recommended.
2. If the Reddit API returns an error due to too many requests, adjust `val` in the instances of `time.sleep(val)` in *explainxkcdbot.py*
