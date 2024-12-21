## How to use it

### Importing markdown files from Obsidian to Pelican 

`obsidian_to_pelican.py` script is used to import your notes from Obsidian and format it properly so it can used by Pelican.

Add the following environment variables to the `.env` file:
- CONTENT_SOURCE_PATH=<your_obsidian_folder>
- IMAGES_SOURCE_PATH=<your_obsidian_image_folder>
- CONTENT_DESTINATION_PATH=<your_pelican_folder/content>
- IMAGES_DESTINATION_PATH=<your_pelican_folder/content/images>

Make sure your files have the following metadata at the top:

- Date: 2024-07-06 23:04
- Category: A category
- Tags: tag1, tag2
- Summary: A summary

There, you can run `publish.sh` script.