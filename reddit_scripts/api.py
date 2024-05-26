from praw import Reddit

from utils.logger import logger

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