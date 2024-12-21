echo "Activating virtual environment"
source env-publishing/bin/activate

echo "Moving files to felipe-arcaro-blog folder..."
python github_pages/obsidian_to_pelican.py

#TBD can trigger ghp from here??

#echo "Publishig to dev.to"
#python dev_to/dev_to_publisher.py
