### Reddit Script
## Features
- Output subscribed subreddit list to txt/csv files

## Prerequisites
To get this script running, you will to create the config for interacting with the Reddit API, and for that you will need to create a [Reddit App](https://business.reddithelp.com/helpcenter/s/article/Create-a-Reddit-Application). 

## Running
- Initialise your environment variables: 
  - `USERNAME`: Your reddit username
  - `PASSWORD`: Your reddit password
  - `CLIENT_ID`: Your reddit script app ID, e.g: 
  - `CLIENT_SECRET`: Your reddit script app secret, e.g: 
  - `USERAGENT`: Should be a unique, descriptive, contain your username on Reddit and the version number of your application. It's used to identify your program. Read more in the documentation [here](https://github.com/reddit-archive/reddit/wiki/API#rules).

- Choose which features you would like to use and write a script in main.py
- Run main.py: 
  ```shell
  python main.py
  ```