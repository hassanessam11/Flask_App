import os
class Config:
    # "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
    # "sqlite:///pythonic.db"
    SECRET_KEY = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
    SQLALCHEMY_DATABASE_URI = "sqlite:///pythonic.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = 'main.upload'