import logging
from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired
import os
import pickle

logger = logging.getLogger(__name__)

SESSION_FILE = "session.pickle"

def save_session(cl):
    with open(SESSION_FILE, "wb") as f:
        pickle.dump(cl.get_settings(), f)

def load_session(cl):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "rb") as f:
            settings = pickle.load(f)
            cl.set_settings(settings)
            try:
                cl.get_timeline_feed()
                logger.info("Logged in using saved session")
                return True
            except Exception:
                logger.warning("Saved session is invalid, logging in again")
    return False

def login_instagram(username, password):
    cl = Client()
    if load_session(cl):
        return cl
    try:
        cl.login(username, password)
        save_session(cl)
        logger.info("Logged in successfully and session saved")
        return cl
    except TwoFactorRequired as e:
        logger.error(" Two-factor authentication is required. Please disable it or use a session login method.")
    except Exception as e:
        logger.error(f"Failed to login to Instagram: {e}")
    return None
