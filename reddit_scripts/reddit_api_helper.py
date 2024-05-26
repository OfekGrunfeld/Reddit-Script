import os
from typing import Union, List
import csv

from praw import Reddit
from prawcore.exceptions import ResponseException

from utils.logger import logger

class RedditAPIHelper:
    def __init__(self, reddit: Reddit, username: str):
        """
        Initialize the RedditAPIHelper class.

        Args:
            reddit (Reddit): Authenticated Reddit API object.
            username (str): The username of the Reddit account.
        """
        self.reddit = reddit
        self.username = username
        self.default_save_name = os.path.join("output", "subreddits")
        self.subreddits_list = []

    def fetch_subscribed(self, return_subreddits: bool = False) -> Union[list[str], None]:
        """
        Get the list of subreddits the user is subscribed to.

        Args:
            return_subreddits (bool): If True, returns the list of subreddits.

        Returns:
            Union[list[str], None]: List of subreddit names or None.
        """
        try:
            logger.debug(f"Fetching subreddits for user {self.username}...")
            self.subreddits_list = [sub.display_name for sub in self.reddit.user.subreddits(limit=None)]
            logger.debug(f"Fetching complete. Found {len(self.subreddits_list)} subreddits for user {self.username}.")
            if return_subreddits:
                return self.subreddits_list
        except ResponseException as error:
            logger.error(f"Couldn't get subreddits list for user {self.username} because of HTTP error: {error}")
        except Exception as error:
            logger.error(f"Error getting subreddits list for user {self.username}: {error}")

    @staticmethod
    def ensure_directory_exists(file_path: str) -> None:
        """
        Ensure the directory for the given file path exists.

        Args:
            file_path (str): The file path for which the directory needs to exist.
        """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def output_subscribed_to_txt(self, file_path: str = None) -> bool:
        """
        Output the subreddit list to a txt file.

        Args:
            file_path (str, optional): The file path to save the txt file. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.subreddits_list:
            logger.debug("No subreddits to output.")
            return False

        default_file_name = os.path.join(self.default_save_name, "subreddits.txt")

        if file_path is None:
            file_path = default_file_name

        if not isinstance(file_path, str):
            logger.debug(f"File path must be a string. Defaulting to {default_file_name}")
            file_path = default_file_name

        RedditAPIHelper.ensure_directory_exists(file_path)

        try:
            with open(file_path, "w") as file:
                file.write("\n".join(self.subreddits_list))
            logger.debug(f"Finished outputting subreddits to {file_path}")
            return True
        except OSError as error:
            logger.error(f"Error writing to file {file_path}: {error}")
            return False
        except Exception as error:
            logger.error(f"Unexpected error saving file to {file_path}: {error}")
            return False

    def output_subscribed_to_csv(self, file_path: str = None) -> bool:
        """
        Output the subreddit list to a csv file.

        Args:
            file_path (str, optional): The file path to save the csv file. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.

        Notes:
            The function is implemented in order to provide support for categorisation of subreddits.
        """
        if not self.subreddits_list:
            logger.debug("No subreddits to output.")
            return False

        default_file_name = os.path.join(self.default_save_name, "subreddits.csv")

        if file_path is None:
            file_path = default_file_name

        if not isinstance(file_path, str):
            logger.debug(f"File path must be a string. Defaulting to {default_file_name}")
            file_path = default_file_name

        RedditAPIHelper.ensure_directory_exists(file_path)

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Subreddits"])
                for subreddit in self.subreddits_list:
                    writer.writerow([subreddit])
            logger.debug(f"Finished outputting subreddits to {file_path}")
            return True
        except OSError as error:
            logger.error(f"Error writing to file {file_path}: {error}")
            return False
        except Exception as error:
            logger.error(f"Unexpected error saving file to {file_path}: {error}")
            return False

    def subscribe_from_list(self, subreddits: List[str]) -> int:
        """
        Subscribe to a list of subreddits.

        Args:
            subreddits (List[str]): List of subreddit names to subscribe to.

        Returns:
            int: Number of successful subscriptions.
        """
        subscribed_count = 0
        for subreddit in subreddits:
            try:
                self.reddit.subreddit(subreddit).subscribe()
                subscribed_count += 1
            except Exception as error:
                logger.error(f"Couldn't subscribe to subreddit {subreddit}. Error: {error}")

        return subscribed_count

    def subscribe_from_txt(self, file_path: str = None) -> int:
        """
        Subscribe to subreddits listed in a text file.

        Returns:
            int: Number of successful subscriptions.
        """
        default_save_path = os.path.join(self.default_save_name, "subreddits.txt")

        if file_path is None or not isinstance(file_path, str):
            file_path = default_save_path
        
        if not isinstance(file_path, str):
            logger.debug(f"File path must be a string. Defaulting to {default_save_path}")
            file_path = default_save_path

        try:
            with open(file_path, "r") as file:
                subreddits = file.read().splitlines()
            logger.debug(f"Read {len(subreddits)} subreddits from {file_path}")
            return self.subscribe_from_list(subreddits)
        except FileNotFoundError as error:
            logger.error(f"File not found: {file_path}")
            return 0
        except Exception as error:
            logger.error(f"Error reading from file {file_path}: {error}")
            return 0


    def fetch_user_moderated_subreddits(self, username: str = None) -> List[str]:
        """
        Fetch the subreddits a specific user moderates.

        Args:
            username (str): The username of the target user.

        Returns:
            List[str]: List of subreddits the user moderates.
        """
        try:
            if username == None:
                logger.debug(f"Received fetch for own user ({username})")
                username = self.username
            logger.debug(f"Fetching moderated subreddits for user {username}...")
            user = self.reddit.redditor(username)
            subreddits = [sub.display_name for sub in user.moderated()]
            logger.debug(f"Fetched {len(subreddits)} moderated subreddits for user {username}.")
            return subreddits
        except ResponseException as error:
            logger.error(f"Couldn't get moderated subreddits list for user {username} because of HTTP error: {error}")
            return []
        except Exception as error:
            logger.error(f"Error getting moderated subreddits list for user {username}: {error}")
            return []
