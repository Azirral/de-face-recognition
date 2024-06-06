import os
import time
from moviepy.editor import VideoFileClip

def get_video_metadata(file_path):
    try:
        # Get the file status
        file_stat = os.stat(file_path)

        # Get the last modified time
        last_modified_time_str = time.ctime(file_stat.st_mtime)
        last_modified_timestamp = int(file_stat.st_mtime)

        # Get the duration of the video
        with VideoFileClip(file_path) as video:
            duration = video.duration

        metadata = {
            'last_modified_time': last_modified_time_str,
            'last_modified_timestamp': last_modified_timestamp,
            'duration': duration  # Duration in seconds
        }

        return metadata

    except FileNotFoundError:
        return f"The file {file_path} does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"
# *Note: you must know the total path to the file.*
# Example usage:
if __name__ == '__main__':
    # Example usage
    file_path = 'C:\\Studiamoje\\Semestr6\\ProjektInżynierski\\DEFaceRecognition\\resources\\s01c01.mp4'  # Replace with your file path
    metadata = get_video_metadata(file_path)
    print(metadata)

