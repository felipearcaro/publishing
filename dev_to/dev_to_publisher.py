from dev_to_client import DevtoClient
from obsidian_handler import ObsidianHandler
import logging

logging.basicConfig(level=logging.DEBUG)

devto_client = DevtoClient()
obsidian_handler = ObsidianHandler()
COMPARISON_PARAMETERS = ['title', 'body_markdown', 'tags', 'published']


def get_payload_from_obsidian(article_file):
    return obsidian_handler.read_mf_file(article_file)


def prepare_obsidian_article_info_for_comparison(obsidian_article_info):
    obsidian_article_info = obsidian_article_info.get('article')
    obsidian_article_info['tags'] = [tag.replace(
        "-", "") for tag in obsidian_article_info.get('tags')]
    return obsidian_article_info


def compare_article_content(article_file, article_info):
    unmatched_parameters = []
    obsidian_article_payload = get_payload_from_obsidian(article_file)
    obsidian_article_info = prepare_obsidian_article_info_for_comparison(
        obsidian_article_payload)
    for parameter in COMPARISON_PARAMETERS:
        logging.debug(f"Comparing article's '{parameter}' information...")
        if obsidian_article_info.get(parameter) != article_info.get(parameter):
            unmatched_parameters.append(parameter)
            logging.debug(f"'{parameter}' parameter has different values")
            ### TEMP ##
            filename = f"{obsidian_article_info.get('title')}_{parameter}.txt"
            with open(filename + "_obsidian", 'w') as file:
                file.write(str(obsidian_article_info.get(parameter)))
            with open(filename + "_devto", 'w') as file:
                file.write(str(article_info.get(parameter)))
            ## TEMP ##
    if unmatched_parameters:
        logging.info(
            f"Article '{article_file}' needs to be updated, the following parameters are not up to date: {unmatched_parameters}")
        update_article(article_info.get('id'), obsidian_article_payload)


def update_article(article_id, payload):
    devto_client.update_article(article_id, payload)


def publish_article(article_file):
    payload = get_payload_from_obsidian(article_file)
    devto_client.publish_article(payload)


# List articles files from Obsidian folder
articles_files = ObsidianHandler().list_articles_files()

for article_file in articles_files:
    logging.info(f"Checking article '{article_file}'...")
    article_info = devto_client.get_article_info_by_title(article_file)
    if article_info:
        logging.info(f"Article '{article_file}' has already been published.")
        compare_article_content(article_file, article_info[0])
    else:
        logging.info(f"Article '{article_file}' has not been published yet.")
        publish_article(article_file)

logging.info(
    f"{devto_client.published_articles} articles were published to dev.to.")
logging.info(
    f"{devto_client.updated_articles} were articles updated to dev.to.")
