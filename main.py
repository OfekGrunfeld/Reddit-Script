from praw import Reddit

from config import get_config
from subreddits import Subreddits

def create_reddit_api_object(config: dict) -> Reddit:
    try:
        reddit = Reddit(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            user_agent=config["user_agent"],
            username=config["username"],
            password=config["password"]
        )
        return reddit
    except KeyError as error:
        raise KeyError(f"Received bad config: {error}")

def test_subreddits():
    config: dict[str, str] = get_config()
    reddit = create_reddit_api_object(config)
    
    subreddits_object = Subreddits(reddit)
    subreddits_object.fetch_subscribed()
    subreddits_object.output_subscribed_to_txt()

    # print(f"Subscribed successfully to: {subreddits_object.subsribe_from_list(["music", "aviation", "formula1"])}")

def main():
    test_subreddits()
    
if __name__ == "__main__":
    main()