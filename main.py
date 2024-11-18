from FileReader import FileReader
from transcript_download import fetch_transcript
import os
from github_transcript_downloader import *

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
    video_id = get_video_id(link)

    if video_id:
        transcript_text = download_transcript(video_id)
        if transcript_text:
            video_title = get_video_title(video_id)
            print(video_title)
            file_name = f"{video_title}.txt"
            file_name = re.sub(r'[\\/*?:"<>|]', '', file_name)  # Remove invalid characters

            file_path = os.path.join(output_dir, file_name)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(transcript_text)

            print(f"Transcript saved to {file_name}")
        else:
            print("Unable to download transcript.")
    else:
        print("Invalid YouTube URL.")