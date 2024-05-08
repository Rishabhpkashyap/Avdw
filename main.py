import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Global dictionary to keep track of downloaded video counts for each URL
download_counts = {}

def find_video_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    video_tag = soup.find('video')
    if video_tag:
        source_tags = video_tag.find_all('source')
        for source_tag in source_tags:
            video_url = source_tag.get('src')
            if video_url:
                return video_url

    return None

def download_video(url, save_dir):
    file_name = url.split('/')[-1]  # Extract file name from URL
    
    # Check if the video URL has been downloaded before
    global download_counts
    if url in download_counts:
        download_counts[url] += 1
        serial_number = download_counts[url]
        save_file_name = f"{file_name}_{serial_number}"
    else:
        download_counts[url] = 1
        save_file_name = file_name
    
    save_path = os.path.join(save_dir, save_file_name)
    
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=save_file_name, position=0, leave=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()

def main():
    webpage_url = input("Enter the URL of the webpage containing the video: ")
    video_url = find_video_url(webpage_url)

    if video_url:
        save_dir = 'downloaded_videos'
        os.makedirs(save_dir, exist_ok=True)
        
        print("Downloading video...")
        try:
            download_video(video_url, save_dir)
            print("Video downloaded successfully.")
        except Exception as e:
            print(f"Error downloading video: {e}")
    else:
        print("No video found on the webpage.")

if __name__ == "__main__":
    main()
