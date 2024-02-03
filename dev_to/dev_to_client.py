import json
import os
import re
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

DEV_TO_INTEGRATION_TOKEN = os.getenv("DEV_TO_INTEGRATION_TOKEN")
CONTENT_START = '## TL;DR'
DEVTO_BASE_URL = 'https://dev.to/api/'
HEADERS = {
    'api-key': DEV_TO_INTEGRATION_TOKEN,
    'Content-Type': 'application/json',
}

logging.basicConfig(level=logging.INFO)


class DevtoClient:

    def __init__(self):
        self.published_articles = 0
        self.updated_articles = 0

    def get_articles(self):
        url = f"{DEVTO_BASE_URL}articles/me"
        response = requests.get(url, headers=HEADERS)
        decoded_response = response.content.decode('utf-8')

        return json.loads(decoded_response)

    def publish_article(self, data: dict):
        url = f"{DEVTO_BASE_URL}articles"
        response = requests.post(url, json=data, headers=HEADERS)
        if response.status_code == 201:
            self.published_articles += 1
            logging.debug('Articled published successfully.')

    def update_article(self, article_id: int, data: dict):
        url = f"{DEVTO_BASE_URL}articles/{article_id}"
        response = requests.put(url, json=data, headers=HEADERS)
        if response.status_code == 200:
            self.updated_articles += 1
            logging.debug('Articled updated successfully.')

    def get_article_info_by_title(self, title: str) -> dict:
        articles = self.get_articles()
        article_info = [{'title': title,
                         'body_markdown': article.get('body_markdown'),
                         'tags': article.get('tag_list'),
                         'published': article.get('published'),
                         'id': article.get('id')}
                        for article in articles if article.get('title') == title]

        return article_info
