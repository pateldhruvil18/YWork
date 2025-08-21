INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "channels",
    "core",
]

ASGI_APPLICATION = "salary_project.asgi.application"

# Channels layer
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# MongoDB (for chat messages) — use djongo or pymongo
from pymongo import MongoClient
MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")
MONGO_DB = MONGO_CLIENT["chat_db"]
