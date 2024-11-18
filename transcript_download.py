import os
import subprocess
from urllib.parse import urlparse, parse_qs

def extract_video_url(playlist_url):
    """
    Extracts the video URL from a YouTube playlist URL.
    
    Args:
        playlist_url (str): The full YouTube playlist URL, which may include video ID, playlist ID, etc.
        
    Returns:
        str: The YouTube video URL without the playlist and other query parameters.
    """
    # Parse the URL
    parsed_url = urlparse(playlist_url)
    print("parsed_url: ", parsed_url)
    
    # Extract the 'v' query parameter (video ID)
    video_id = parse_qs(parsed_url.query).get('v', [None])[0]
    print("video_id: ", video_id)
    
    # Check if video ID is found
    if video_id:
        # Return the YouTube video URL
        print("Returning this: ", f"https://www.youtube.com/watch?v={video_id}")
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        raise ValueError("Video ID not found in the provided URL")


def fetch_video_title(video_url):
    """
    Fetch the video title using yt-dlp.
    Args:
        video_url (str): The URL of the YouTube video.
    Returns:
        str: The title of the video.
    """

    try:
        # Use yt-dlp to extract video information in JSON format
        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--print", "title", video_url],
            capture_output=True,
            text=True,
            check=True,
        )
        title = result.stdout.strip()
        return title
    except subprocess.CalledProcessError as e:
        print(f"Error fetching title for {video_url}: {e}")
        return None

def fetch_transcript(video_url, output_dir):
    """
    Fetch the transcript of a YouTube video using yt-dlp.
    Args:
        video_url (str): The URL of the YouTube video.
        output_dir (str): Directory where the transcript will be saved.
    """
    
    video_url = extract_video_url(playlist_url=video_url)

    # Get video title for the file name
    title = fetch_video_title(video_url)
    print("Title of video: ", title)
    if not title:
        print(f"Skipping {video_url} due to missing title.")
        return

    # Sanitize title to avoid invalid file names
    sanitized_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
    transcript_file = os.path.join(output_dir, f"{sanitized_title}.en.vtt")
    output_template = os.path.join(output_dir, f"{sanitized_title}.%(ext)s")

    try:
        # Use yt-dlp to fetch the transcript
        print(f"Processing: {video_url} ({sanitized_title})")
        subprocess.run(
            [
                "yt-dlp",
                "--write-auto-sub",  # Download auto-generated subtitles
                "--sub-lang", "en",  # Language code for English subtitles
                "--skip-download",  # Do not download the video
                "-o", output_template,  # Save subtitles with title as the filename
                video_url,
            ],
            check=True,
        )

        # Rename to .txt format for easier reading
        if os.path.exists(transcript_file):
            txt_file = transcript_file.replace(".en.vtt", ".txt")
            os.rename(transcript_file, txt_file)
            print(f"Transcript saved: {txt_file}")
        else:
            print(f"No transcript available for: {video_url}")

    except subprocess.CalledProcessError as e:
        print(f"Error fetching transcript for {video_url}: {e}")


