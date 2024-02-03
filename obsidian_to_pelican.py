import shutil
import os
import re
from dotenv import load_dotenv

load_dotenv()

CONTENT_SOURCE_PATH = os.getenv("CONTENT_SOURCE_PATH")
IMAGES_SOURCE_PATH = os.getenv("IMAGES_SOURCE_PATH")
CONTENT_DESTINATION_PATH = os.getenv("CONTENT_DESTINATION_PATH")
IMAGES_DESTINATION_PATH = os.getenv("IMAGES_DESTINATION_PATH")
LINK_SYNTAX = "{filename}"
IMAGE_SYNTAX = "{attach}"
IMAGE_CSS_CLASS = "{: .image-process-large-photo}"


def replace_image_reference(content):
    """
        Replace Obsidian with Pelican image reference.
        E.g. ![[image.png]] >> ![image]({attach}/images/image.png){: .image-process-large-photo}
    """

    pattern = r"!\[\[(.*?)\.(?:png|jpg|jpeg)\]\]"
    matches = re.findall(pattern, content)

    for image_title in matches:
        replacement = "![" + image_title + \
            "](" + IMAGE_SYNTAX + "/images/" + \
            image_title + ".png)" + IMAGE_CSS_CLASS
        content = content.replace("![[" + image_title + ".png]]", replacement)

    return content


def rename_file(filename: str) -> str:
    """
        Convert file name to lowercase with underscores.
    """

    return filename.replace(" ", "_").lower()


def replace_internal_link(content) -> str:
    """
        Replace Obsidian with Pelican internal links
        E.g. [[Another page]] >> [Another page]({filename}/another_page.md)
    """

    pattern = r"(?<!!)\[\[(.*?)\]\]"
    matches = re.findall(pattern, content)

    for file_title in matches:

        file_name = rename_file(file_title)
        replacement = "[" + file_title + \
            "](" + LINK_SYNTAX + "/" + file_name + ".md)"
        content = content.replace("[[" + file_title + "]]", replacement)

    return content


def clear_content_folder():
    """
    Clear up content folder.
    """
    if os.path.exists(CONTENT_DESTINATION_PATH) and os.path.isdir(CONTENT_DESTINATION_PATH):
        shutil.rmtree(CONTENT_DESTINATION_PATH)

    os.makedirs(CONTENT_DESTINATION_PATH)
    print("Content folder has been cleared out.")


def copy_images_folder():
    """
        Copy images folder from Obsidian to content folder.
    """
    print("Copying images folder...")
    try:
        shutil.copytree(IMAGES_SOURCE_PATH, IMAGES_DESTINATION_PATH)
    except FileExistsError as e:
        print(e)


if __name__ == "__main__":

    clear_content_folder()

    copy_images_folder()

    # Copy markdown files from Obsidian Vault to Pelican project
    for file in os.listdir(CONTENT_SOURCE_PATH):
        file_path = os.path.join(CONTENT_SOURCE_PATH, file)

        print(f"Copying {file}...")

        # Read the original file
        with open(file_path, "r") as f:
            content = f.read()

        new_filename = rename_file(file)
        new_filepath = os.path.join(CONTENT_DESTINATION_PATH, new_filename)

        content = replace_internal_link(content)

        content = replace_image_reference(content)

        # Add title to the top of the file
        title = os.path.splitext(file)[0]
        content_with_title = f"Title: {title}\n{content}"

        # Write the modified content to the new file
        with open(new_filepath, "w") as f:
            f.write(content_with_title)
