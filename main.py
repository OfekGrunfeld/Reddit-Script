from praw import Reddit
from config import config

from subreddits import Subreddits
from logger import logger

def create_reddit_api_object(config: dict) -> Reddit:
    """
    Create and authenticate a Reddit API object.

    Args:
        config (dict): Configuration dictionary containing Reddit API credentials.

    Returns:
        Reddit: Authenticated Reddit API object.
    """
    try:
        logger.debug("Logging in to Reddit API...")
        reddit = Reddit(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            user_agent=config["user_agent"],
            username=config["username"],
            password=config["password"]
        )
        logger.debug("Logging successful!")
        return reddit
    except KeyError as error:
        logger.error(f"Received bad config: {error}")
        raise KeyError(f"Received bad config: {error}")

def test_subreddits():
    reddit = create_reddit_api_object(config)
    
    subreddits_object = Subreddits(reddit, config["username"])
    subreddits_object.fetch_subscribed()
    subreddits_object.output_subscribed_to_txt()

    logger.debug(f"Output to txt success: {subreddits_object.output_subscribed_to_txt()}")
    logger.debug(f"Output to csv success: {subreddits_object.output_subscribed_to_csv()}")

def main():
    test_subreddits()
    
if __name__ == "__main__":
    main()
