import os
from typing import Union
import csv

from praw import Reddit
from prawcore.exceptions import ResponseException

class Subreddits:
    def __init__(self, reddit: Reddit):
        self.reddit = reddit
        self.default_save_name = os.path.join("output", "subreddits", "subreddits")
        self.subreddits_list = []

    def fetch_subscribed(self, return_subreddits: bool = False) -> Union[list[str], None]:
        """
        Get the list of subreddits the user is subscribed to.
        """
        try:
            print("Fetching user subreddits...")
            self.subreddits_list = [sub.display_name for sub in self.reddit.user.subreddits(limit=None)]
            print(f"Fetching complete. Found {len(self.subreddits_list)} subreddits")
            if return_subreddits:
                return self.subreddits_list
        except ResponseException as error:
            print(f"Couldn't get user subreddits list because of HTTP error: {error}")
        except Exception as error:
            print(f"Error getting subreddits list: {error}")

    def ensure_directory_exists(self, file_path: str) -> None:
        """Ensure the directory for the given file path exists."""
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def output_subscribed_to_txt(self, file_path: str = None) -> bool:
        """
        Output the subreddit list to a txt file.

        Returns:
            bool: Success
        """
        if not self.subreddits_list:
            print("No subreddits to output.")
            return False

        default_file_name = f"{self.default_save_name}.txt"

        if file_path is None:
            file_path = default_file_name

        if not isinstance(file_path, str):
            print(f"File path must be a string. Defaulting to {default_file_name}")
            file_path = default_file_name

        self.ensure_directory_exists(file_path)

        try:
            with open(file_path, "w") as file:
                file.write("\n".join(self.subreddits_list))
            print(f"Finished outputting subreddits to {file_path}")
            return True
        except OSError as error:
            print(f"Error writing to file {file_path}: {error}")
            return False
        except Exception as error:
            print(f"Unexpected error saving file to {file_path}: {error}")
            return False

    def output_subscribed_to_csv(self, file_path: str = None) -> bool:
        """
        Output the subreddit list to a csv file.

        Returns:
            bool: Success
        """
        if not self.subreddits_list:
            print("No subreddits to output.")
            return False

        default_file_name = f"{self.default_save_name}.csv"

        if file_path is None:
            file_path = default_file_name

        if not isinstance(file_path, str):
            print(f"File path must be a string. Defaulting to {default_file_name}")
            file_path = default_file_name

        self.ensure_directory_exists(file_path)

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Subreddits"])
                for subreddit in self.subreddits_list:
                    writer.writerow([subreddit])
            print(f"Finished outputting subreddits to {file_path}")
            return True
        except OSError as error:
            print(f"Error writing to file {file_path}: {error}")
            return False
        except Exception as error:
            print(f"Unexpected error saving file to {file_path}: {error}")
            return False

    def subscribe_from_list(self, subreddits: list[str]) -> int:
        """
        Subscribe to a list of subreddits.

        Returns:
            int: Number of successful subscriptions.
        """
        subscribed_count = 0
        for subreddit in subreddits:
            try:
                self.reddit.subreddit(subreddit).subscribe()
                subscribed_count += 1
            except Exception as error:
                print(f"Couldn't subscribe to subreddit {subreddit}. Error: {error}")

        return subscribed_count