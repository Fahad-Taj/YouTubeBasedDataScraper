from FileReader import FileReader
from transcript_download import fetch_transcript
import os

def create_directory(directory_name):
    """Create a subdirectory if it does not exist."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

output_dir = "downloaded_transcripts"
create_directory(output_dir)

FILE_NAME = "links.txt"

file_reader = FileReader(FILE_NAME)
links = file_reader.read_file() # 'links' is a list which contains all the links as strings

for link in links:
    print("link: ", link)
    fetch_transcript(link, "Data Structures and Algorithms in Python - Greg Hogg")