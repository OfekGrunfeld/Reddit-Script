from dotenv import load_dotenv
import os

def get_config() -> dict[str, str]:
    load_dotenv()
    config = {}
    config["client_id"] = os.getenv("CLIENT_ID")
    config["client_secret"] = os.getenv("CLIENT_SECRET")
    config["user_agent"] = os.getenv("USERAGENT")
    config["username"] = os.getenv("USERNAME")
    config["password"] = os.getenv("PASSWORD")

    return config