import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

def get_kite_secret():
    kite_secret = dict()
    kite_secret["api_key"]=os.getenv("KITE_API_KEY")
    kite_secret["api_secret"]=os.getenv("KITE_API_SECRET")
    return kite_secret

def get_admin_secret():
    admin_secret = dict()
    admin_secret["userid"]=os.getenv("ADMIN_ID")
    admin_secret["password"]=os.getenv("ADMIN_PASSWORD")
    admin_secret["image"]=os.getenv("ADMIN_IMAGE_URL")
    return admin_secret