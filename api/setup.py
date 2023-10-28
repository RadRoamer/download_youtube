import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()
API_KEY = os.getenv('API_KEY')
VERSION = 'v3'
NAME = 'youtube'
youtube = build(NAME, VERSION, developerKey=API_KEY)
DEFAULT_DOWN_PATH = r'D:\\'

