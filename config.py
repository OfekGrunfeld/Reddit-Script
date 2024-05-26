from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET"),
    "user_agent": os.getenv("USERAGENT"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
}