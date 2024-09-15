import os

class Config:
    # SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
    SECRET_KEY = os.urandom(24)