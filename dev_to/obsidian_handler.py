import os
import re
from dotenv import load_dotenv

load_dotenv()

CONTENT_SOURCE_PATH = os.getenv("CONTENT_SOURCE_PATH")
FILE_FORMAT = ".md"
CONTENT_START = "## TL;DR"
SERIES_START = "####"
GITHUB_IMAGES_LINK = os.getenv("GITHUB_IMAGES_LINK")

class ObsidianHandler:
    
    def list_articles_files(self) -> list:
        articles_files = []
        for article_file in os.listdir(CONTENT_SOURCE_PATH):
            file_name, file_format = os.path.splitext(article_file)
            if file_format == FILE_FORMAT:
                articles_files.append(file_name)

        return articles_files
    

    def format_payload(self, title, content, tags, series):
        
        payload = {
            "article": {
                "title": title,
                "published": True,
                "series": series,
                "body_markdown": content,
                "tags": tags
            }
        }
        
        return payload

    def __get_image_references(self, content):
        
        pattern = r"!\[\[(.*?)\.(?:png|jpg|jpeg)\]\]"
        matches = re.findall(pattern, content)

        for image_title in matches:
            replacement = "![" + image_title + "](" + GITHUB_IMAGES_LINK + image_title + ".png)" 
            content = content.replace("![[" + image_title + ".png]]", replacement)

        return content

    def read_mf_file(self, file_name: str) -> dict:
        with open (f"{CONTENT_SOURCE_PATH}/{file_name}{FILE_FORMAT}") as file:
            markdown_content = file.read()
            tags_match = re.search(r"^Tags: (.+)", markdown_content, re.MULTILINE)
            series_match = re.search(r"#### (.+)", markdown_content, re.MULTILINE)
            content = CONTENT_START + markdown_content.split(CONTENT_START)[1]
            content = self.__get_image_references(content)

        title = file_name
        tags = [tag.strip() for tag in tags_match.group(1).split(',')] if tags_match else []
        series = series_match.group(1).strip() if series_match else None 
        payload = self.format_payload(title, content, tags, series)
        
        return payload