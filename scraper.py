from playwright.sync_api import sync_playwright
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


with open("config.json") as f:
    config = json.load(f)

URLS = config["urls"]
EMAIL = config["email"]

SEEN_FILE = "seen.json"

SELECTORS = {
    "trackr": "a.text-trackr-link-blue",
    "brightnetwork": "a[href*='/graduate-jobs/']",
    "gradcracker": "a[href*='/graduate-job/']"
}