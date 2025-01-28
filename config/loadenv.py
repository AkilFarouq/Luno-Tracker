import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_URL = os.getenv("API_URL")
API_BAL_URL = os.getenv("API_BAL_URL")
API_TRANS_URL = os.getenv("API_TRANS_URL")
TRANS_DIR=os.getenv("TRANS_DIR")
COMP_DIR=os.getenv("COMP_DIR")